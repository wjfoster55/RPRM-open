"""Passive dual-domain 1-D conservative tracer (MODFLOW 6 GWT + IST).

Separately specified successor to verification problem 6.3.2:
no production, no sorption, nonreacting tracer only.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from pprint import pformat
from typing import Literal

import flopy
import numpy as np

from .paths import ROOT, mf6

ControlKind = Literal["dual_slow", "no_immobile", "rapid_equilibration"]


@dataclass(frozen=True)
class PassiveColumnSpec:
    """Physically legible 1-D dual-domain column."""

    name: str = "passive_dd"
    nlay: int = 1
    nrow: int = 1
    ncol: int = 101
    delr: float = 1.0
    delc: float = 1.0
    top: float = 1.0
    botm: float = 0.0
    specific_discharge: float = 0.1  # m/d
    al: float = 1.0  # m longitudinal dispersivity
    volfrac: float = 0.25
    porosity_mobile: float = 0.25
    porosity_immobile: float = 0.10
    zetaim: float = 5.0e-3  # 1/d slow exchange
    pulse_conc: float = 1.0
    pulse_duration: float = 50.0  # d
    total_time: float = 400.0  # d
    nstp_pulse: int = 25
    nstp_flush: int = 100
    obs_x: float = 50.0  # m
    control: ControlKind = "dual_slow"

    def effective_zeta(self) -> float:
        if self.control == "no_immobile":
            return 0.0
        if self.control == "rapid_equilibration":
            return 10.0  # 1/d, intentionally fast vs pulse/flush scale
        return self.zetaim

    def use_ist(self) -> bool:
        return self.control != "no_immobile"


@dataclass(frozen=True)
class EpisodeResult:
    name: str
    control: str
    times: list[float]
    outlet_c: list[float]
    mobile_mass: list[float]
    immobile_mass: list[float]
    mass_residual_rel: float
    notes: str


def _ws(spec: PassiveColumnSpec, base: Path | None = None) -> Path:
    base = base or (ROOT / "experiments" / "passive_dual_domain" / "runs")
    return base / spec.name / spec.control


def build_flow(spec: PassiveColumnSpec, base: Path | None = None):
    name = "flow"
    sim_ws = _ws(spec, base) / "mf6gwf"
    sim = flopy.mf6.MFSimulation(sim_name=name, sim_ws=sim_ws, exe_name=mf6())
    tdis_ds = (
        (spec.pulse_duration, 1, 1.0),
        (spec.total_time - spec.pulse_duration, 1, 1.0),
    )
    flopy.mf6.ModflowTdis(sim, nper=2, perioddata=tdis_ds, time_units="days")
    flopy.mf6.ModflowIms(sim)
    gwf = flopy.mf6.ModflowGwf(sim, modelname=name, save_flows=True)
    flopy.mf6.ModflowGwfdis(
        gwf,
        length_units="meters",
        nlay=spec.nlay,
        nrow=spec.nrow,
        ncol=spec.ncol,
        delr=spec.delr,
        delc=spec.delc,
        top=spec.top,
        botm=spec.botm,
    )
    flopy.mf6.ModflowGwfnpf(
        gwf,
        save_specific_discharge=True,
        save_saturation=True,
        icelltype=0,
        k=1.0,
    )
    flopy.mf6.ModflowGwfic(gwf, strt=spec.top)
    flopy.mf6.ModflowGwfchd(
        gwf, stress_period_data=[[(0, 0, spec.ncol - 1), spec.top]]
    )
    q = spec.specific_discharge * spec.delc * spec.top
    wel_spd = {0: [[(0, 0, 0), q]], 1: [[(0, 0, 0), q]]}
    flopy.mf6.ModflowGwfwel(gwf, stress_period_data=wel_spd, pname="WEL-1")
    flopy.mf6.ModflowGwfoc(
        gwf,
        head_filerecord=f"{name}.hds",
        budget_filerecord=f"{name}.bud",
        saverecord=[("HEAD", "ALL"), ("BUDGET", "ALL")],
    )
    return sim


def build_transport(spec: PassiveColumnSpec, base: Path | None = None):
    name = "trans"
    sim_ws = _ws(spec, base) / "mf6gwt"
    sim = flopy.mf6.MFSimulation(sim_name=name, sim_ws=sim_ws, exe_name=mf6())
    tdis_ds = (
        (spec.pulse_duration, spec.nstp_pulse, 1.0),
        (spec.total_time - spec.pulse_duration, spec.nstp_flush, 1.0),
    )
    flopy.mf6.ModflowTdis(sim, nper=2, perioddata=tdis_ds, time_units="days")
    flopy.mf6.ModflowIms(sim, linear_acceleration="bicgstab")
    gwt = flopy.mf6.ModflowGwt(sim, modelname=name, save_flows=True)
    flopy.mf6.ModflowGwtdis(
        gwt,
        length_units="meters",
        nlay=spec.nlay,
        nrow=spec.nrow,
        ncol=spec.ncol,
        delr=spec.delr,
        delc=spec.delc,
        top=spec.top,
        botm=spec.botm,
    )
    flopy.mf6.ModflowGwtic(gwt, strt=0.0)
    # Passive: no decay, no sorption
    if spec.use_ist():
        mst_porosity = spec.porosity_mobile / (1.0 - spec.volfrac)
    else:
        mst_porosity = spec.porosity_mobile
    flopy.mf6.ModflowGwtmst(gwt, porosity=mst_porosity)
    if spec.use_ist():
        flopy.mf6.ModflowGwtist(
            gwt,
            porosity=spec.porosity_immobile / spec.volfrac,
            volfrac=spec.volfrac,
            zetaim=spec.effective_zeta(),
            cim_filerecord=f"{name}.cim",
        )
    flopy.mf6.ModflowGwtadv(gwt)
    flopy.mf6.ModflowGwtdsp(gwt, xt3d_off=True, alh=spec.al, ath1=spec.al)
    flopy.mf6.ModflowGwtfmi(
        gwt,
        packagedata=[
            ("GWFHEAD", "../mf6gwf/flow.hds", None),
            ("GWFBUDGET", "../mf6gwf/flow.bud", None),
        ],
    )
    cnc_spd = {
        0: [[(0, 0, 0), spec.pulse_conc]],
        1: [[(0, 0, 0), 0.0]],
    }
    flopy.mf6.ModflowGwtcnc(gwt, stress_period_data=cnc_spd)
    flopy.mf6.ModflowGwtssm(gwt, sources=[[]])
    obsj = min(spec.ncol - 1, max(0, int(round(spec.obs_x / spec.delr))))
    flopy.mf6.ModflowUtlobs(
        gwt,
        digits=10,
        print_input=True,
        continuous={
            f"{name}.obs.csv": [
                ("outlet", "CONCENTRATION", (0, 0, obsj)),
            ]
        },
    )
    flopy.mf6.ModflowGwtoc(
        gwt,
        budget_filerecord=f"{name}.cbc",
        concentration_filerecord=f"{name}.ucn",
        saverecord=[("CONCENTRATION", "ALL"), ("BUDGET", "ALL")],
    )
    return sim


def run_episode(spec: PassiveColumnSpec, base: Path | None = None, silent: bool = True) -> EpisodeResult:
    flow = build_flow(spec, base=base)
    trans = build_transport(spec, base=base)
    flow.write_simulation(silent=silent)
    trans.write_simulation(silent=silent)
    ok, buff = flow.run_simulation(silent=silent, report=True)
    assert ok, pformat(buff)
    ok, buff = trans.run_simulation(silent=silent, report=True)
    assert ok, pformat(buff)

    ws = _ws(spec, base)
    obs = flopy.utils.Mf6Obs(ws / "mf6gwt" / "trans.obs.csv").data
    times = [float(t) for t in obs["totim"]]
    outlet = [float(c) for c in obs["OUTLET"]]

    # Mass accounting from concentration files (cell volumes * porosity factors)
    cell_vol = spec.delr * spec.delc * (spec.top - spec.botm)
    ucn = flopy.utils.HeadFile(ws / "mf6gwt" / "trans.ucn", text="CONCENTRATION")
    mobile_mass: list[float] = []
    immobile_mass: list[float] = []
    cim_path = ws / "mf6gwt" / "trans.cim"
    cim = None
    if spec.use_ist() and cim_path.exists():
        cim = flopy.utils.HeadFile(cim_path, text="CIM")

    for kstpkper in ucn.get_kstpkper():
        cm = np.asarray(ucn.get_data(kstpkper=kstpkper), dtype=float).ravel()
        if spec.use_ist():
            vm = cell_vol * (1.0 - spec.volfrac) * (spec.porosity_mobile / (1.0 - spec.volfrac))
            # simplifies to cell_vol * porosity_mobile
            vm = cell_vol * spec.porosity_mobile
            mm = float(np.sum(cm * vm))
            if cim is not None:
                ci = np.asarray(cim.get_data(kstpkper=kstpkper), dtype=float).ravel()
                vi = cell_vol * spec.volfrac * (spec.porosity_immobile / spec.volfrac)
                # simplifies to cell_vol * porosity_immobile
                vi = cell_vol * spec.porosity_immobile
                im = float(np.sum(ci * vi))
            else:
                im = float("nan")
        else:
            mm = float(np.sum(cm * cell_vol * spec.porosity_mobile))
            im = 0.0
        mobile_mass.append(mm)
        immobile_mass.append(im)

    # Cheap residual proxy: final total aqueous mass vs peak total (not a full budget audit)
    tot = np.asarray(mobile_mass, dtype=float) + np.nan_to_num(
        np.asarray(immobile_mass, dtype=float), nan=0.0
    )
    peak = float(np.max(tot)) if len(tot) else 0.0
    residual = float(abs(tot[-1]) / peak) if peak > 0 else 0.0

    return EpisodeResult(
        name=spec.name,
        control=spec.control,
        times=times,
        outlet_c=outlet,
        mobile_mass=mobile_mass,
        immobile_mass=immobile_mass,
        mass_residual_rel=residual,
        notes=(
            f"Passive tracer; control={spec.control}; "
            f"zeta_eff={spec.effective_zeta()}; spec={asdict(spec)}"
        ),
    )
