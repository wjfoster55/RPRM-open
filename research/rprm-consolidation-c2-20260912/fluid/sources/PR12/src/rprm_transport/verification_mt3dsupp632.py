"""Official MT3DMS Supplemental Guide Problem 6.3.2 via FloPy + local binaries.

This reproduces the published verification problem (production ± sorption).
It is NOT the passive-tracer scientific model.
"""

from __future__ import annotations

from pathlib import Path
from pprint import pformat

import flopy
import numpy as np

from .paths import ROOT, mf2005, mf6, mt3dms

# Official scenario parameters (Zheng 2010 / MF6 examples notebook)
PARAMETERS = {
    "ex-gwt-mt3dsupp632a": {
        "distribution_coefficient": 0.25,
        "decay": 0.0,
        "decay_sorbed": -1.0e-3,
    },
    "ex-gwt-mt3dsupp632b": {
        "distribution_coefficient": 0.25,
        "decay": -5.0e-4,
        "decay_sorbed": -5.0e-4,
    },
    "ex-gwt-mt3dsupp632c": {
        "distribution_coefficient": 0.0,
        "decay": -1.0e-3,
        "decay_sorbed": 0.0,
    },
}

LENGTH_UNITS = "meters"
TIME_UNITS = "days"
NPER = 2
NLAY = 1
NROW = 1
NCOL = 401
DELR = 2.5
DELC = 1.0
TOP = 1.0
BOTM = 0.0
SPECIFIC_DISCHARGE = 0.06
LONGITUDINAL_DISPERSIVITY = 10.0
VOLFRAC = 0.2
POROSITY = 0.2
POROSITY_IMMOBILE = 0.05
BULK_DENSITY = 4.0
ZETA_IM = 1.0e-3
SOURCE_DURATION = 1000.0
TOTAL_TIME = 10000.0
OBS_XLOC = 200.0
ZERO_ORDER_DECAY = True
DUAL_DOMAIN = True


def _workspace(sim_folder: str, base: Path | None = None) -> Path:
    base = base or (ROOT / "experiments" / "verification_mt3dsupp632" / "runs")
    return base / sim_folder


def build_mf6gwf(sim_folder: str, base: Path | None = None):
    name = "flow"
    sim_ws = _workspace(sim_folder, base) / "mf6gwf"
    sim = flopy.mf6.MFSimulation(sim_name=name, sim_ws=sim_ws, exe_name=mf6())
    tdis_ds = (
        (SOURCE_DURATION, 1, 1.0),
        (TOTAL_TIME - SOURCE_DURATION, 1, 1.0),
    )
    flopy.mf6.ModflowTdis(sim, nper=NPER, perioddata=tdis_ds, time_units=TIME_UNITS)
    flopy.mf6.ModflowIms(sim)
    gwf = flopy.mf6.ModflowGwf(sim, modelname=name, save_flows=True)
    flopy.mf6.ModflowGwfdis(
        gwf,
        length_units=LENGTH_UNITS,
        nlay=NLAY,
        nrow=NROW,
        ncol=NCOL,
        delr=DELR,
        delc=DELC,
        top=TOP,
        botm=BOTM,
    )
    flopy.mf6.ModflowGwfnpf(
        gwf,
        save_specific_discharge=True,
        save_saturation=True,
        icelltype=0,
        k=1.0,
    )
    flopy.mf6.ModflowGwfic(gwf, strt=1.0)
    flopy.mf6.ModflowGwfchd(gwf, stress_period_data=[[(0, 0, NCOL - 1), 1.0]])
    wel_spd = {
        0: [[(0, 0, 0), SPECIFIC_DISCHARGE * DELC * TOP]],
        1: [[(0, 0, 0), SPECIFIC_DISCHARGE * DELC * TOP]],
    }
    flopy.mf6.ModflowGwfwel(gwf, stress_period_data=wel_spd, pname="WEL-1")
    flopy.mf6.ModflowGwfoc(
        gwf,
        head_filerecord=f"{name}.hds",
        budget_filerecord=f"{name}.bud",
        saverecord=[("HEAD", "ALL"), ("BUDGET", "ALL")],
    )
    return sim


def build_mf6gwt(
    sim_folder: str,
    distribution_coefficient: float,
    decay: float,
    decay_sorbed: float,
    base: Path | None = None,
):
    name = "trans"
    sim_ws = _workspace(sim_folder, base) / "mf6gwt"
    sim = flopy.mf6.MFSimulation(sim_name=name, sim_ws=sim_ws, exe_name=mf6())
    pertim1 = SOURCE_DURATION
    pertim2 = TOTAL_TIME - SOURCE_DURATION
    tdis_ds = ((pertim1, 10, 1.0), (pertim2, 90, 1.0))
    flopy.mf6.ModflowTdis(sim, nper=NPER, perioddata=tdis_ds, time_units=TIME_UNITS)
    flopy.mf6.ModflowIms(sim, linear_acceleration="bicgstab")
    gwt = flopy.mf6.ModflowGwt(sim, modelname=name, save_flows=True)
    flopy.mf6.ModflowGwtdis(
        gwt,
        length_units=LENGTH_UNITS,
        nlay=NLAY,
        nrow=NROW,
        ncol=NCOL,
        delr=DELR,
        delc=DELC,
        top=TOP,
        botm=BOTM,
    )
    first_order_decay = not ZERO_ORDER_DECAY
    if distribution_coefficient > 0:
        sorption = "linear"
        bd = BULK_DENSITY
        kd = distribution_coefficient
    else:
        sorption = None
        bd = None
        kd = None
    flopy.mf6.ModflowGwtic(gwt, strt=0)
    flopy.mf6.ModflowGwtmst(
        gwt,
        zero_order_decay=ZERO_ORDER_DECAY,
        first_order_decay=first_order_decay,
        sorption=sorption,
        porosity=POROSITY / (1.0 - VOLFRAC),
        decay=decay,
        decay_sorbed=decay_sorbed,
        bulk_density=bd,
        distcoef=kd,
    )
    if DUAL_DOMAIN:
        flopy.mf6.ModflowGwtist(
            gwt,
            zero_order_decay=ZERO_ORDER_DECAY,
            first_order_decay=first_order_decay,
            sorption=sorption,
            porosity=POROSITY_IMMOBILE / VOLFRAC,
            volfrac=VOLFRAC,
            zetaim=ZETA_IM,
            decay=decay,
            decay_sorbed=decay_sorbed,
            bulk_density=bd,
            distcoef=kd,
            cim_filerecord=f"{name}.cim",
        )
    flopy.mf6.ModflowGwtadv(gwt)
    flopy.mf6.ModflowGwtdsp(
        gwt,
        xt3d_off=True,
        alh=LONGITUDINAL_DISPERSIVITY,
        ath1=LONGITUDINAL_DISPERSIVITY,
    )
    pd = [
        ("GWFHEAD", "../mf6gwf/flow.hds", None),
        ("GWFBUDGET", "../mf6gwf/flow.bud", None),
    ]
    flopy.mf6.ModflowGwtfmi(gwt, packagedata=pd)
    cnc_spd = {
        0: [[(0, 0, 0), 1.0]],
        1: [[(0, 0, 0), 0.0]],
    }
    flopy.mf6.ModflowGwtcnc(gwt, stress_period_data=cnc_spd)
    flopy.mf6.ModflowGwtssm(gwt, sources=[[]])
    obsj = int(OBS_XLOC / DELR) + 1
    obs_data = {
        f"{name}.obs.csv": [
            ("myobs", "CONCENTRATION", (0, 0, obsj)),
        ],
    }
    flopy.mf6.ModflowUtlobs(gwt, digits=10, print_input=True, continuous=obs_data)
    flopy.mf6.ModflowGwtoc(
        gwt,
        budget_filerecord=f"{name}.cbc",
        concentration_filerecord=f"{name}.ucn",
        saverecord=[("CONCENTRATION", "LAST"), ("BUDGET", "LAST")],
    )
    return sim


def build_mf2005(sim_folder: str, base: Path | None = None):
    name = "flow"
    sim_ws = _workspace(sim_folder, base) / "mf2005"
    mf = flopy.modflow.Modflow(modelname=name, model_ws=sim_ws, exe_name=mf2005())
    perlen = [SOURCE_DURATION, TOTAL_TIME - SOURCE_DURATION]
    flopy.modflow.ModflowDis(
        mf,
        nlay=NLAY,
        nrow=NROW,
        ncol=NCOL,
        delr=DELR,
        delc=DELC,
        top=TOP,
        botm=BOTM,
        nper=NPER,
        perlen=perlen,
    )
    flopy.modflow.ModflowBas(mf)
    flopy.modflow.ModflowLpf(mf)
    flopy.modflow.ModflowPcg(mf)
    flopy.modflow.ModflowLmt(mf)
    flopy.modflow.ModflowChd(mf, stress_period_data=[[0, 0, NCOL - 1, 1.0, 1.0]])
    wel_spd = {
        0: [[0, 0, 0, SPECIFIC_DISCHARGE * DELC * TOP]],
        1: [[0, 0, 0, SPECIFIC_DISCHARGE * DELC * TOP]],
    }
    flopy.modflow.ModflowWel(mf, stress_period_data=wel_spd)
    return mf


def build_mt3dms(
    sim_folder: str,
    distribution_coefficient: float,
    decay: float,
    decay_sorbed: float,
    modflowmodel,
    base: Path | None = None,
):
    name = "trans"
    sim_ws = _workspace(sim_folder, base) / "mt3d"
    mt = flopy.mt3d.Mt3dms(
        modelname=name,
        model_ws=sim_ws,
        exe_name=mt3dms(),
        modflowmodel=modflowmodel,
        ftlfilename="../mf2005/mt3d_link.ftl",
    )
    dt0 = SOURCE_DURATION / 10.0
    flopy.mt3d.Mt3dBtn(mt, laycon=0, prsity=POROSITY, obs=[(0, 0, 81)], dt0=dt0, ifmtcn=1)
    flopy.mt3d.Mt3dAdv(mt, mixelm=0)
    flopy.mt3d.Mt3dDsp(mt, al=LONGITUDINAL_DISPERSIVITY)
    sp1 = distribution_coefficient
    sp2 = 0.0
    rc1 = decay
    rc2 = decay_sorbed
    prsity2 = 0.0
    if DUAL_DOMAIN:
        prsity2 = POROSITY_IMMOBILE
        if distribution_coefficient > 0:
            isothm = 6
            sp2 = ZETA_IM
        else:
            isothm = 5
            sp2 = ZETA_IM
            rc2 = 0.0
    else:
        isothm = 1
        if distribution_coefficient <= 0:
            rc2 = 0
    ireact = 100 if ZERO_ORDER_DECAY else 1
    flopy.mt3d.Mt3dRct(
        mt,
        isothm=isothm,
        ireact=ireact,
        igetsc=0,
        rhob=BULK_DENSITY,
        sp1=sp1,
        sp2=sp2,
        prsity2=prsity2,
        rc1=rc1,
        rc2=rc2,
    )
    ssm_spd = {0: [0, 0, 0, 1.0, -1], 1: [0, 0, 0, 0.0, -1]}
    flopy.mt3d.Mt3dSsm(mt, stress_period_data=ssm_spd)
    flopy.mt3d.Mt3dGcg(mt)
    return mt


def build_models(sim_name: str, base: Path | None = None, **params):
    sim_mf6gwf = build_mf6gwf(sim_name, base=base)
    sim_mf6gwt = build_mf6gwt(sim_name, base=base, **params)
    sim_mf2005 = build_mf2005(sim_name, base=base)
    sim_mt3dms = build_mt3dms(sim_name, modflowmodel=sim_mf2005, base=base, **params)
    return sim_mf6gwf, sim_mf6gwt, sim_mf2005, sim_mt3dms


def write_models(sims, silent: bool = True):
    sim_mf6gwf, sim_mf6gwt, sim_mf2005, sim_mt3dms = sims
    sim_mf6gwf.write_simulation(silent=silent)
    sim_mf6gwt.write_simulation(silent=silent)
    sim_mf2005.write_input()
    sim_mt3dms.write_input()


def run_models(sims, silent: bool = True):
    sim_mf6gwf, sim_mf6gwt, sim_mf2005, sim_mt3dms = sims
    success, buff = sim_mf6gwf.run_simulation(silent=silent, report=True)
    assert success, pformat(buff)
    success, buff = sim_mf6gwt.run_simulation(silent=silent, report=True)
    assert success, pformat(buff)
    success, buff = sim_mf2005.run_model(silent=silent, report=True)
    assert success, pformat(buff)
    success, buff = sim_mt3dms.run_model(
        silent=silent, normal_msg="Program completed", report=True
    )
    assert success, pformat(buff)


def load_observation_pair(sim_name: str, base: Path | None = None):
    ws = _workspace(sim_name, base)
    mf6_csv = ws / "mf6gwt" / "trans.obs.csv"
    mf6_ra = flopy.utils.Mf6Obs(mf6_csv).data
    mt_obs = ws / "mt3d" / "MT3D001.OBS"
    mt_ra = flopy.mt3d.Mt3dms.load_obs(mt_obs)
    return mf6_ra, mt_ra


def max_abs_rel_diff(sim_name: str, base: Path | None = None) -> float:
    """Compare MF6 and MT3DMS observation series on overlapping times (interpolated)."""
    mf6_ra, mt_ra = load_observation_pair(sim_name, base=base)
    t_mf6 = np.asarray(mf6_ra["totim"], dtype=float)
    c_mf6 = np.asarray(mf6_ra["MYOBS"], dtype=float)
    t_mt = np.asarray(mt_ra["time"], dtype=float)
    # MT3DMS OBS columns include step/time plus one or more cell labels like "(1, 1, 82)"
    skip = {"step", "time", "kstep", "kstp", "kper"}
    mt_cols = [c for c in mt_ra.dtype.names if c.lower() not in skip]
    if not mt_cols:
        raise ValueError(f"No concentration columns in MT3DMS OBS: {mt_ra.dtype.names}")
    c_mt = np.asarray(mt_ra[mt_cols[0]], dtype=float)
    c_mt_i = np.interp(t_mf6, t_mt, c_mt)
    denom = np.maximum(np.abs(c_mt_i), 1e-12)
    return float(np.max(np.abs(c_mf6 - c_mt_i) / denom))


def run_scenario(idx: int, base: Path | None = None, silent: bool = True) -> dict:
    key = list(PARAMETERS.keys())[idx]
    params = PARAMETERS[key]
    sims = build_models(key, base=base, **params)
    write_models(sims, silent=silent)
    run_models(sims, silent=silent)
    rel = max_abs_rel_diff(key, base=base)
    return {"scenario": key, "params": params, "max_abs_rel_diff_vs_mt3dms": rel}
