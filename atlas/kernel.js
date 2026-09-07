/* RPRM Mechanical Motion Atlas: finite ideal model laws and typed composition.
 * IEEE-754 evaluations are numerical samples, not exact inverse-fiber solutions.
 * Display output/hidden channels and full typed component outputs are distinct.
 */
globalThis.MMAKernel = (() => {
  "use strict";
  const TAU = 2 * Math.PI;
  let state;
  const clamp = (value, low, high) => Math.max(low, Math.min(high, value));
  const fract = value => value - Math.floor(value);
  const mod = (value, base) => ((value % base) + base) % base;
  const smoothstep = value => {
    const x = clamp(value, 0, 1);
    return x * x * (3 - 2 * x);
  };
  const triangle = theta => 2 / Math.PI * Math.asin(Math.sin(theta));
  const anglePoint = (center, radius, angle) => [
    center[0] + radius * Math.cos(angle),
    center[1] + radius * Math.sin(angle)
  ];

  function universalAngle(theta, beta) {
    const cycle = Math.floor((theta + Math.PI) / TAU);
    const local = theta - cycle * TAU;
    return Math.atan2(Math.cos(beta) * Math.sin(local), Math.cos(local)) + cycle * TAU;
  }

  function sliderPosition(theta, radius = 1, rod = 3) {
    return radius * Math.cos(theta) + Math.sqrt(Math.max(0, rod * rod - radius * radius * Math.sin(theta) ** 2));
  }

  function chebyshev(theta) {
    const o1 = [0, 0];
    const o2 = [2, 0];
    const a = [Math.cos(theta), Math.sin(theta)];
    const radius = 2.5;
    const dx = o2[0] - a[0];
    const dy = o2[1] - a[1];
    const distance = Math.hypot(dx, dy);
    const half = distance / 2;
    const height = Math.sqrt(Math.max(0, radius * radius - half * half));
    const middle = [(a[0] + o2[0]) / 2, (a[1] + o2[1]) / 2];
    const offset = [-dy / distance * height, dx / distance * height];
    const b = [middle[0] + offset[0], middle[1] + offset[1]];
    const p = [2 * b[0] - a[0], 2 * b[1] - a[1]];
    return { o1, o2, a, b, p };
  }

  function absCosIntegral(theta) {
    const sign = theta < 0 ? -1 : 1;
    const x = Math.abs(theta);
    const periods = Math.floor(x / Math.PI);
    const remainder = x - periods * Math.PI;
    const tail = remainder <= Math.PI / 2 ? Math.sin(remainder) : 2 - Math.sin(remainder);
    return sign * (2 * periods + tail);
  }

  function gatedAdvance(theta, start, width) {
    const turns = theta / TAU;
    const whole = Math.floor(turns);
    const phase = fract(turns);
    let local = 0;
    if (phase >= start + width) local = 1;
    else if (phase > start) local = smoothstep((phase - start) / width);
    return whole + local;
  }

  const mechanisms = [
    {
      id: "schmidt", n: 1, name: "Schmidt coupling", short: "Schmidt", family: "transport",
      map: "parallel-offset rotation → rotation",
      formula: "φ = θ; middle disc translates twice per turn",
      rprm: "CAR only for retained shaft phase; offset accommodation is a typed adapter.",
      fiber: "ONE on the declared phase/branch; dropping the middle disc forgets internal translation.",
      fidelity: "Exact ideal phase law; center-disc motion is schematic.",
      parameter: a => `radial offset proxy ${(0.18 + 0.52 * a).toFixed(2)}`,
      output: theta => Math.sin(theta),
      hidden: theta => Math.cos(2 * theta)
    },
    {
      id: "cv", n: 2, name: "Constant-velocity joint", short: "CV joint", family: "transport",
      map: "angled-axis rotation → rotation",
      formula: "φ = θ + φ₀ (ideal CV constraint)",
      rprm: "Phase CAR at fixed geometry; the joint internals are outside the displayed receiver.",
      fiber: "ONE for ideal retained phase; internal contact paths are forgotten.",
      fidelity: "Exact ideal transfer law; 2D joint drawing is schematic.",
      parameter: a => `shaft bend ${(8 + 52 * a).toFixed(0)}°`,
      output: theta => Math.sin(theta),
      hidden: (theta, a) => Math.sin(theta) * Math.sin((8 + 52 * a) * Math.PI / 180)
    },
    {
      id: "universal", n: 3, name: "Single Cardan (universal) joint", short: "Universal joint", family: "transport",
      map: "angled-axis rotation → nonuniform rotation",
      formula: "φ = atan2(cos β · sin θ, cos θ)",
      rprm: "Phase can remain a CAR at fixed β; constant-rate transport fails under the speed receiver.",
      fiber: "ONE phase map for |β|<90°; speed alone has MANY phase preimages.",
      fidelity: "Exact ideal Cardan phase law.",
      parameter: a => `shaft bend ${(8 + 52 * a).toFixed(0)}°`,
      output: (theta, a) => Math.sin(universalAngle(theta, (8 + 52 * a) * Math.PI / 180)),
      hidden: (theta, a) => {
        const beta = (8 + 52 * a) * Math.PI / 180;
        return Math.cos(beta) / (1 - Math.sin(beta) ** 2 * Math.sin(theta) ** 2) - 1;
      }
    },
    {
      id: "bevel", n: 4, name: "Bevel gear pair", short: "Bevel gear pair", family: "ratio",
      map: "rotation → right-angle rotation",
      formula: "φ = −(Nᵢ/Nₒ) θ",
      rprm: "A direction/ratio adapter; a CAR needs full tooth address and a declared common closure.",
      fiber: "Bare wrapped angle can be MANY when the ratio covers the output circle.",
      fidelity: "Exact ideal no-slip gear ratio.",
      parameter: a => `ratio ${(0.5 + 1.5 * a).toFixed(2)}:1`,
      output: (theta, a) => Math.sin(-(0.5 + 1.5 * a) * theta),
      hidden: (theta, a) => Math.sin((6 + Math.round(8 * a)) * theta)
    },
    {
      id: "slider", n: 5, name: "Slider-crank linkage", short: "Slider-crank", family: "convert",
      map: "rotation → reciprocating translation",
      formula: "x = r cos θ + √(ℓ² − r² sin² θ)",
      rprm: "Deterministic full-configuration adapter; piston-only projection is a FOLD.",
      fiber: "Piston x is generally MANY(2) over a cycle; crank phase restores ONE.",
      fidelity: "Exact ideal planar linkage constraint.",
      parameter: a => `rod/crank ratio ${(2.2 + 2.8 * a).toFixed(2)}`,
      output: (theta, a) => sliderPosition(theta, 1, 2.2 + 2.8 * a),
      hidden: (theta, a) => Math.asin(Math.sin(theta) / (2.2 + 2.8 * a))
    },
    {
      id: "sun-planet", n: 6, name: "Sun-and-planet converter", short: "Sun + planet", family: "convert",
      map: "rotation ↔ beam stroke with 2:1 closure",
      formula: "beam proxy q = cos(θ/2)",
      rprm: "Ratio-plus-conversion adapter; the beam receiver forgets gear contact and driver phase.",
      fiber: "Beam position is MANY; full gear/contact state is required for inversion.",
      fidelity: "Normalized half-angle beam proxy; not a complete epicyclic mechanism model.",
      parameter: a => `orbit radius ${(0.24 + 0.20 * a).toFixed(2)}`,
      output: theta => Math.cos(theta / 2),
      hidden: theta => Math.sin(theta)
    },
    {
      id: "scotch", n: 7, name: "Scotch yoke", short: "Scotch yoke", family: "convert",
      map: "rotation → sinusoidal translation",
      formula: "x = r cos θ",
      rprm: "Exact coordinate adapter into a slider receiver; projection alone is a FOLD.",
      fiber: "Slider x is MANY(2) except at extrema; phase plus orientation restores ONE.",
      fidelity: "Exact ideal planar constraint.",
      parameter: a => `stroke radius ${(0.22 + 0.28 * a).toFixed(2)}`,
      output: theta => Math.cos(theta),
      hidden: theta => Math.sin(theta)
    },
    {
      id: "chebyshev", n: 8, name: "Chebyshev Lambda linkage", short: "Chebyshev λ", family: "convert",
      map: "rotation → approximate straight-line foot path",
      formula: "|A−B|=|B−O₂|=2.5; P=2B−A",
      rprm: "Full branch-fixed geometry is ONE; the nearly straight foot coordinate is an approximate ADAPTER/FOLD, not automatically a CAR.",
      fiber: "Crank phase + assembly branch gives ONE configuration; a line coordinate can have MANY preimages.",
      fidelity: "Exact ideal linkage at normalized lengths 1, 2, 2.5, 2.5.",
      parameter: a => `straightness gate ε = ${(0.5 + 4.5 * a).toFixed(1)}% (receiver only)`,
      output: theta => chebyshev(theta).p[0],
      hidden: theta => chebyshev(theta).p[1] - 4.0
    },
    {
      id: "chain", n: 9, name: "Chain drive", short: "Chain drive", family: "transport",
      map: "rotation → displaced rotation",
      formula: "φ = +(Nᵢ/Nₒ) θ (no slip)",
      rprm: "Tooth-address transport; the chain carries phase across spatial separation.",
      fiber: "ONE with retained tooth addresses and closure; bare wrapped phase may be MANY.",
      fidelity: "Exact ideal no-slip ratio; polygonal speed ripple omitted.",
      parameter: a => `sprocket ratio ${(0.55 + 1.45 * a).toFixed(2)}:1`,
      output: (theta, a) => Math.sin((0.55 + 1.45 * a) * theta),
      hidden: (theta, a) => Math.sin((8 + Math.round(12 * a)) * theta) * 0.1
    },
    {
      id: "belt", n: 10, name: "Belt drive", short: "Belt drive", family: "transport",
      map: "rotation → displaced rotation",
      formula: "φ = +(Rᵢ/Rₒ) θ (open, no slip)",
      rprm: "Phase adapter under a no-slip contract; elastic stretch and slip reopen the seam.",
      fiber: "ONE only in the declared no-slip model; otherwise OPEN without belt-state receipts.",
      fidelity: "Exact ideal ratio; elasticity and slip omitted.",
      parameter: a => `pulley ratio ${(0.55 + 1.45 * a).toFixed(2)}:1`,
      output: (theta, a) => Math.sin((0.55 + 1.45 * a) * theta),
      hidden: (theta, a) => Math.sin(theta - (0.55 + 1.45 * a) * theta)
    },
    {
      id: "gearbox", n: 11, name: "Constant-mesh gearbox", short: "Gearbox", family: "ratio",
      map: "selected gear pair → output rotation",
      formula: "φ = −gₖ θ; k selected by dog clutch",
      rprm: "A finite selector chooses one typed ratio adapter; selection is load-bearing state.",
      fiber: "ONE with gear, dog, tooth address, and direction retained; output alone is MANY.",
      fidelity: "Exact ideal selected ratio; engagement transient omitted.",
      parameter: a => `selected ratio ${[0.5, 1, 2][Math.min(2, Math.floor(a * 3))].toFixed(1)}:1`,
      output: (theta, a) => Math.sin(-[0.5, 1, 2][Math.min(2, Math.floor(a * 3))] * theta),
      hidden: (_theta, a) => Math.min(2, Math.floor(a * 3)) - 1
    },
    {
      id: "oscillator", n: 12, name: "Oscillatory reverser", short: "Oscillatory reverser", family: "gate",
      map: "continuous rotation → alternating rotation",
      formula: "φ = A(2/π) asin(sin θ)",
      rprm: "A direction-changing adapter; output angle forgets which half-cycle supplied it.",
      fiber: "MANY(2) for most output angles; phase/direction receipt restores the branch.",
      fidelity: "Normalized constant-speed reversal idealization; changeover dynamics omitted.",
      parameter: a => `swing amplitude ${(0.25 + 0.75 * a).toFixed(2)}`,
      output: (theta, a) => (0.25 + 0.75 * a) * triangle(theta),
      hidden: theta => Math.sign(Math.cos(theta))
    },
    {
      id: "limiter", n: 13, name: "Torque-limiting clutch", short: "Torque limiter", family: "gate",
      map: "rotation + load → tracked rotation or slip",
      formula: "τload≤τlim ⇒ φ=θ; else slip",
      rprm: "A threshold gate that deliberately breaks phase CAR when load exceeds the aperture.",
      fiber: "Overload output is not invertible without load and slip history; often MANY or OPEN.",
      fidelity: "Threshold idealization; no elastic/friction dynamics.",
      parameter: a => `load/limit ${(0.45 + 1.45 * a).toFixed(2)}`,
      output: (theta, a) => {
        const load = 0.45 + 1.45 * a;
        return Math.sin(theta * Math.min(1, 1 / load));
      },
      hidden: (_theta, a) => 1 - Math.min(1, 1 / (0.45 + 1.45 * a))
    },
    {
      id: "winch", n: 14, name: "Winch", short: "Winch", family: "accumulate",
      map: "rotation → accumulated rope travel",
      formula: "s = r θ (constant-radius ideal)",
      rprm: "An unwrapped coordinate CAR only while radius, layer, and rope attachment stay retained.",
      fiber: "ONE on a bounded unwrapped interval; wrapped phase forgets winding count.",
      fidelity: "Exact constant-radius idealization; changing spool radius omitted.",
      parameter: a => `drum radius ${(0.18 + 0.32 * a).toFixed(2)}`,
      output: (theta, a) => (0.18 + 0.32 * a) * theta,
      hidden: theta => theta / TAU
    },
    {
      id: "rack", n: 15, name: "Rack-and-pinion", short: "Rack + pinion", family: "convert",
      map: "rotation ↔ translation",
      formula: "x = r θ (no slip, finite rack)",
      rprm: "A genuine bounded coordinate CAR when unwrapped angle, rack interval, and no-slip contact are retained.",
      fiber: "ONE inside the admitted rack interval; wrapped angle or end-stop contact reopens it.",
      fidelity: "Exact ideal pitch-line kinematics.",
      parameter: a => `pitch radius ${(0.18 + 0.32 * a).toFixed(2)}`,
      output: (theta, a) => (0.18 + 0.32 * a) * theta,
      hidden: theta => fract(theta / TAU) * 2 - 1
    },
    {
      id: "offset", n: 16, name: "Eccentric contact-gated drive", short: "Contact-gated drive", family: "gate",
      map: "eccentric rotation → intermittent rotation",
      formula: "q = floor(t) + smooth contact pulse",
      rprm: "A contact-gated accumulator; the dwell receiver is a lossy FOLD of driver phase.",
      fiber: "Every dwell interval is MANY; exact reopen needs eccentric phase and contact state.",
      fidelity: "Normalized contact-window model, not an involute gear solver.",
      parameter: a => `contact window ${(0.12 + 0.43 * a).toFixed(2)} turn`,
      output: (theta, a) => gatedAdvance(theta, 0.12, 0.12 + 0.43 * a),
      hidden: (theta, a) => {
        const phase = fract(theta / TAU);
        return phase > 0.12 && phase < 0.24 + 0.43 * a ? 1 : 0;
      }
    },
    {
      id: "one-way", n: 17, name: "One-way mechanical rectifier", short: "One-way rectifier", family: "gate",
      map: "bidirectional oscillation → one-direction accumulation",
      formula: "ωₒ = |ωᵢ| for θᵢ = sin t",
      rprm: "A rectifying FOLD: it retains magnitude/progress and forgets the input direction sign.",
      fiber: "At least MANY(2) in the rate receiver; history needs the ordered sign word to reopen.",
      fidelity: "Exact ideal rectifier law; ratchet backlash omitted.",
      parameter: a => `output gain ${(0.35 + 1.15 * a).toFixed(2)}`,
      output: (theta, a) => (0.35 + 1.15 * a) * absCosIntegral(theta),
      hidden: theta => Math.sign(Math.cos(theta))
    },
    {
      id: "cam", n: 18, name: "Cam-and-follower", short: "Cam + follower", family: "convert",
      map: "rotation + profile → follower lift",
      formula: "h(θ) = max(0, cos θ)² (chosen profile)",
      rprm: "The cam is a physical lookup adapter; the lift receiver forgets phase across dwells.",
      fiber: "MANY throughout dwell and generally MANY(2) on symmetric rise/fall.",
      fidelity: "Exact chosen display profile; not a universal cam law.",
      parameter: a => `lift ${(0.20 + 0.70 * a).toFixed(2)}`,
      output: (theta, a) => (0.20 + 0.70 * a) * Math.max(0, Math.cos(theta)) ** 2,
      hidden: theta => Math.cos(theta) > 0 ? 1 : 0
    },
    {
      id: "intermittent", n: 19, name: "Pin-and-slot indexing stage", short: "Indexing stage", family: "gate",
      map: "continuous rotation → indexed advance; hold supplied separately",
      formula: "q = floor(t) + S(contact); native hold is OPEN",
      rprm: "Engagement GATE plus accumulator; positive hold is OPEN until a holding stage such as the worm is composed.",
      fiber: "A displayed dwell merges MANY driver phases; without a retained holder, physical output phase is not fixed.",
      fidelity: "Normalized advance law; a positive holding constraint is not supplied by this model.",
      parameter: a => `advance window ${(0.10 + 0.32 * a).toFixed(2)} turn`,
      output: (theta, a) => gatedAdvance(theta, 0.08, 0.10 + 0.32 * a),
      hidden: (theta, a) => {
        const phase = fract(theta / TAU);
        return phase > 0.08 && phase < 0.18 + 0.32 * a ? 1 : 0;
      }
    },
    {
      id: "worm", n: 20, name: "Worm gear set", short: "Worm gear", family: "ratio",
      map: "screw rotation → high-reduction rotation",
      formula: "φ = −(starts/Nwheel) θ",
      rprm: "Ideal tooth transport is a ratio adapter; physical self-locking is a separate directional gate.",
      fiber: "ONE with tooth address and winding retained; backdrive disposition depends on friction/lead angle.",
      fidelity: "Exact ideal ratio; self-locking physics omitted.",
      parameter: a => `reduction 1:${Math.round(12 + 48 * a)}`,
      output: (theta, a) => Math.sin(-theta / Math.round(12 + 48 * a)),
      hidden: theta => fract(theta / TAU) * 2 - 1
    }
  ];


  const STUDIO_PORTS = Object.freeze({
    schmidt: ["rotary.phase", "rotary.phase"],
    cv: ["rotary.phase", "rotary.phase"],
    universal: ["rotary.phase", "rotary.phase"],
    bevel: ["rotary.phase", "rotary.phase"],
    slider: ["rotary.phase", "linear.position"],
    "sun-planet": ["rotary.phase", "linear.position"],
    scotch: ["rotary.phase", "linear.position"],
    chebyshev: ["rotary.phase", "path.xy"],
    chain: ["rotary.phase", "rotary.phase"],
    belt: ["rotary.phase", "rotary.phase"],
    gearbox: ["rotary.phase", "rotary.phase"],
    oscillator: ["rotary.phase", "rotary.phase"],
    limiter: ["rotary.phase", "rotary.phase"],
    winch: ["rotary.phase", "length.unwrapped"],
    rack: ["rotary.phase", "linear.position"],
    offset: ["rotary.phase", "rotary.phase"],
    "one-way": ["rotary.phase", "rotary.unwrapped"],
    cam: ["rotary.phase", "linear.position"],
    intermittent: ["rotary.phase", "rotary.phase"],
    worm: ["rotary.phase", "rotary.phase"]
  });
  const STUDIO_ADAPTERS = Object.freeze({
    "rotary.unwrapped→rotary.phase": { kind: "ADAPTER", note: "retain winding and fold to declared phase" },
    "rotary.phase→rotary.unwrapped": { kind: "ADAPTER", note: "retain a winding sheet on the finite input interval" },
    "length.unwrapped→linear.position": { kind: "ADAPTER", note: "declare guide frame, origin, and admitted interval" },
    "linear.position→length.unwrapped": { kind: "ADAPTER", note: "declare oriented payout route and admitted interval" },
    "time.turns→rotary.phase": { kind: "ADAPTER", note: "multiply turns by τ and retain the clock origin" },
    "path.1d→linear.position": { kind: "ADAPTER", note: "select the one retained path coordinate" },
    "path.2d→path.xy": { kind: "CAR", note: "rename the retained ordered x/y coordinate pair" },
    "path.2d→linear.position": { kind: "FOLD", note: "project the retained path to x; y becomes a reopen obligation" },
    "path.3d→path.xy": { kind: "FOLD", note: "project x/y and omit z at this two-coordinate receiver" }
  });


const byId=new Map(mechanisms.map(m=>[m.id,m]));
  function studioCoreComponents() {
    const sources = [
      { id: "motor", name: "Rotary motor", family: "source", inPort: null, outPort: "rotary.phase", operation: "DRIVE", note: "Finite live phase source." },
      { id: "clock", name: "Turn clock", family: "source", inPort: null, outPort: "time.turns", operation: "DRIVE", note: "Unwrapped input-turn coordinate." },
      { id: "address-clock", name: "Strong address clock", family: "source", inPort: null, outPort: "strong.address", operation: "DRIVE", note: "Bounded address source on the current 2n carrier." },
      { id: "digit-clock", name: "Radix-10 digit source", family: "source", inPort: null, outPort: "digit.base10", operation: "DRIVE", note: "Cycles through the declared finite digit carrier 0..9." },
      { id: "carry-one", name: "Carry-in 1", family: "source", inPort: null, outPort: "carry.bit", operation: "DRIVE", note: "One declared incoming carry occurrence; not inferred from screen contact." },
      { id: "zip-carrier", name: "Cyclic half-turn", family: "carrier", inPort: "strong.address", outPort: "strong.address", operation: "PORTAL", note: "Applies D(d)=d+n mod 2n; relationship type stays PORTAL." },
      { id: "carry-cell", name: "Local radix-10 carry cell", family: "carrier", inputPorts: [{ name: "digit", type: "digit.base10" }, { name: "carry", type: "carry.bit" }], inPort: "digit.base10 + carry.bit", outPort: "digit-carry.base10", operation: "FOLD", note: "(q,r)=divmod(d+c,10); deterministic and conserving. Bare output is MANY(2) internally except (0,0),(0,1); the incoming carry receipt reopens ONE." },
      { id: "carry-digit-fold", name: "Carry-cell digit projection", family: "receiver", inPort: "digit-carry.base10", outPort: "digit.base10", operation: "FOLD", note: "Projects r and retains the complete pair only through the upstream receipt." },
      { id: "carry-out-fold", name: "Carry-cell carry projection", family: "receiver", inPort: "digit-carry.base10", outPort: "carry.bit", operation: "FOLD", note: "Projects q for a next local cell; the digit branch remains in the upstream receipt." },
      { id: "trace-receiver", name: "Trace receiver", family: "receiver", inPort: "receiver.any", outPort: "receipt.trace", operation: "FOLD", note: "Captures one typed input and retains its source-port receipt." }
    ];
    const zipper = [
      { id: "odd-path-clock", name: "Path address source", family: "source", inPort: null, outPort: "absolute.address", operation: "DRIVE", note: "One retained address x in the frozen path 1..9." },
      ...[2, 4, 6, 8].map(center => ({ id: `zip-chart-${center}`, name: `Coordinate chart c=${center}`, family: "carrier", inPort: "absolute.address", outPort: "chart.coordinate", operation: "CAR", note: `h_${center}(x)=x-${center} on [${center - 1},${center},${center + 1}].` })),
      ...[3, 5, 7].map(point => ({ id: `zip-handoff-${point}`, name: `Handoff port x=${point}`, family: "receiver", inputPorts: [{ name: "left", type: "chart.coordinate" }, { name: "right", type: "chart.coordinate" }], inPort: "left + right chart coordinates", outPort: "handoff.receipt", operation: "CHECK", note: `Checks the same absolute point ${point} as +1 left and -1 right; overlap is not a seam.` }))
    ];
    const mechanismComponents = mechanisms.map(mechanism => ({
      id: mechanism.id,
      name: mechanism.name,
      family: mechanism.family,
      inPort: STUDIO_PORTS[mechanism.id][0],
      outPort: STUDIO_PORTS[mechanism.id][1],
      operation: mechanism.rprm.startsWith("CAR") ? "CAR" : "ADAPTER",
      note: mechanism.map
    }));
    return [...sources, ...zipper, ...mechanismComponents];
  }

  function studioComponentDefinition(componentId) {
    const core = studioCoreComponents().find(component => component.id === componentId);
    if (core) return core;
    return null;
  }

  function studioNodeDefinition(node) {
    return node ? studioComponentDefinition(node.componentId) : null;
  }

  function studioDefinitionInputPorts(definition) {
    if (!definition) return [];
    if (Array.isArray(definition.inputPorts) && definition.inputPorts.length) {
      return definition.inputPorts.map(port => ({ name: String(port.name), type: String(port.type) }));
    }
    return definition.inPort ? [{ name: "in", type: definition.inPort }] : [];
  }

  function studioInputPort(definition, requestedPort = null) {
    const ports = studioDefinitionInputPorts(definition);
    return ports.find(port => port.name === requestedPort) || (requestedPort == null ? ports[0] || null : null);
  }

  function studioConnectionDisposition(fromNode, toNode, targetPort = null) {
    const source = studioNodeDefinition(fromNode);
    const target = studioNodeDefinition(toNode);
    return studioDefinitionConnectionDisposition(source, target, targetPort);
  }

  function studioDefinitionConnectionDisposition(source, target, targetPort = null) {
    if (!source || !target) return { kind: "OPEN_TYPED_ADAPTER", note: "component definition missing" };
    if (!source.outPort) return { kind: "OPEN_TYPED_ADAPTER", note: `${source.name} exposes no output port` };
    const port = studioInputPort(target, targetPort);
    if (!port) return { kind: "OPEN_TYPED_ADAPTER", note: targetPort == null ? `${target.name} is a source and exposes no input port` : `${target.name} has no ${targetPort} input aperture` };
    if (port.type === "receiver.any") return { kind: "FOLD", note: `retain ${source.outPort} as the receiver source-port receipt` };
    if (source.outPort === port.type) return { kind: "EXACT", note: `${port.name} accepts ${port.type}; no screen geometry is used` };
    return STUDIO_ADAPTERS[`${source.outPort}→${port.type}`] || {
      kind: "OPEN_TYPED_ADAPTER",
      note: `no declared ${source.outPort} → ${port.type} bridge for ${target.name}:${port.name}`
    };
  }

  function studioMechanismOutput(componentId, input, aperture) {
    const scalar = Array.isArray(input) ? input[0] : input;
    if (!Number.isFinite(scalar)) return NaN;
    if (componentId === "schmidt" || componentId === "cv") return scalar;
    if (componentId === "universal") return universalAngle(scalar, (8 + 52 * aperture) * Math.PI / 180);
    if (componentId === "bevel") return -(0.5 + 1.5 * aperture) * scalar;
    if (componentId === "slider") return sliderPosition(scalar, 1, 2.2 + 2.8 * aperture);
    if (componentId === "sun-planet") return Math.cos(scalar / 2);
    if (componentId === "scotch") return (0.22 + 0.28 * aperture) * Math.cos(scalar);
    if (componentId === "chebyshev") {
      const point = chebyshev(scalar).p;
      return [point[0], point[1]];
    }
    if (componentId === "chain" || componentId === "belt") return (0.55 + 1.45 * aperture) * scalar;
    if (componentId === "gearbox") return -[0.5, 1, 2][Math.min(2, Math.floor(aperture * 3))] * scalar;
    if (componentId === "oscillator") return (0.25 + 0.75 * aperture) * triangle(scalar);
    if (componentId === "limiter") return scalar * Math.min(1, 1 / (0.45 + 1.45 * aperture));
    if (componentId === "winch" || componentId === "rack") return (0.18 + 0.32 * aperture) * scalar;
    if (componentId === "offset") return gatedAdvance(scalar, 0.12, 0.12 + 0.43 * aperture) * TAU;
    if (componentId === "one-way") return (0.35 + 1.15 * aperture) * absCosIntegral(scalar);
    if (componentId === "cam") return (0.20 + 0.70 * aperture) * Math.max(0, Math.cos(scalar)) ** 2;
    if (componentId === "intermittent") return gatedAdvance(scalar, 0.08, 0.10 + 0.32 * aperture) * TAU;
    if (componentId === "worm") return -scalar / Math.round(12 + 48 * aperture);
    return NaN;
  }

  function studioApplyComponent(node, definition, input) {
    const studio = state.studio;
    if (definition.id === "motor") return { status: "ONE", value: studio.phase * TAU, note: "live rotary phase" };
    if (definition.id === "clock") return { status: "ONE", value: studio.phase, note: "live input turns" };
    if (definition.id === "digit-clock") return { status: "ONE", value: Math.floor(fract(studio.phase) * 10), note: "digit address in retained base-10 carrier" };
    if (definition.id === "carry-one") return { status: "ONE", value: 1, note: "declared incoming carry occurrence" };
    if (definition.id === "address-clock") {
      const carrierN = Number.isInteger(node.frozenParameters?.n) ? node.frozenParameters.n : state.zip.n;
      return { status: "ONE", value: Math.floor(fract(studio.phase) * 2 * carrierN), note: `strong address in retained C_${2 * carrierN}` };
    }
    if (definition.id === "zip-carrier") {
      const carrierN = Number.isInteger(node.frozenParameters?.n) ? node.frozenParameters.n : state.zip.n;
      return Number.isFinite(Number(input))
      ? { status: "ONE", value: zipD(Math.round(Number(input)), carrierN), note: `PORTAL applied D on retained C_${2 * carrierN}; not a universal collision response` }
      : { status: "NONE", value: null, note: "PORTAL requires one admitted strong address" };
    }
    if (definition.id === "carry-cell") {
      const digit = Number(input?.digit?.value), carryIn = Number(input?.carry?.value);
      if (!Number.isInteger(digit) || digit < 0 || digit > 9 || ![0, 1].includes(carryIn)) return { status: "NONE", value: null, note: "local carry requires d in 0..9 and c in {0,1}" };
      const sum = digit + carryIn, q = Math.floor(sum / 10), r = sum % 10;
      const bareFiber = (r === 0 && (q === 0 || q === 1)) ? "ONE" : "MANY(2)";
      return { status: "ONE", value: [r, q], note: `d+c=${digit}+${carryIn}=${r}+10×${q} · bare output ${bareFiber} · ONE with incoming-carry receipt` };
    }
    if (definition.id === "carry-digit-fold" || definition.id === "carry-out-fold") {
      if (!Array.isArray(input) || input.length !== 2 || input.some(value => !Number.isInteger(Number(value)))) return { status: "NONE", value: null, note: "projection requires one retained [digit,carry] pair" };
      const index = definition.id === "carry-digit-fold" ? 0 : 1;
      return { status: "ONE", value: Number(input[index]), note: `${index ? "carry q" : "digit r"} projected; sibling channel retained only by reopening the source receipt` };
    }
    if (definition.id === "odd-path-clock") return { status: "ONE", value: state.studio.coordinateZipper.point, note: "retained absolute address in 1..9" };
    if (definition.id.startsWith("zip-chart-")) {
      const center = Number(definition.id.split("-").at(-1)), x = Math.round(Number(input));
      return Number.isInteger(x) && Math.abs(x - center) <= 1 ? { status: "ONE", value: x - center, note: `absolute ${x} has local coordinate ${x - center} in chart c=${center}` } : { status: "OPEN", value: null, note: `absolute address is outside chart c=${center}` };
    }
    if (definition.id.startsWith("zip-handoff-")) {
      const point = Number(definition.id.split("-").at(-1)), left = Number(input?.left?.value), right = Number(input?.right?.value);
      return left === 1 && right === -1 ? { status: "ONE", value: point, note: `typed handoff at absolute ${point}; +1 → -1 without global negation` } : { status: "OPEN", value: null, note: `handoff ${point} requires the paired (+1,-1) chart receipts` };
    }
    if (definition.id === "trace-receiver") return { status: "ONE", value: input, note: "receiver Fold retains the incoming port on the edge receipt" };
    if (byId.has(definition.id)) {
      const value = studioMechanismOutput(definition.id, input, node.aperture);
      const finite = Array.isArray(value) ? value.every(Number.isFinite) : Number.isFinite(value);
      return finite ? { status: "ONE", value, note: `${definition.operation} evaluated on the selected ideal branch` } : { status: "NONE", value: null, note: "mechanism left its admitted numeric branch" };
    }
    return { status: "OPEN", value: null, note: "OPEN_UNSUPPORTED: component runtime is not registered" };
  }

  function studioTransmit(value, sourcePort, targetPort, disposition, exactValue = null) {
    if (disposition.kind === "OPEN_TYPED_ADAPTER") return { status: "OPEN", value: null };
    if (sourcePort === "time.turns" && targetPort === "rotary.phase") return { status: "ONE", value: Number(value) * TAU, exactValue: null };
    if (Array.isArray(value) && (targetPort === "linear.position" || targetPort === "path.xy")) return { status: "ONE", value: targetPort === "path.xy" ? value.slice(0, 2) : value[0], exactValue: null };
    return { status: "ONE", value, exactValue };
  }

  function studioEvaluation() {
    const studio = state.studio;
    const results = new Map();
    const diagnostics = [];
    const incoming = new Map(studio.nodes.map(node => [node.id, []]));
    studio.edges.forEach(edge => {
      if (incoming.has(edge.to)) incoming.get(edge.to).push(edge);
    });
    const unresolved = new Set(studio.nodes.map(node => node.id));
    let changed = true;
    while (changed) {
      changed = false;
      for (const node of studio.nodes) {
        if (!unresolved.has(node.id)) continue;
        const definition = studioNodeDefinition(node);
        if (!definition) {
          results.set(node.id, { status: "OPEN", value: null, note: "missing component definition" });
          unresolved.delete(node.id);
          changed = true;
          continue;
        }
        const edges = incoming.get(node.id) || [];
        const inputPorts = studioDefinitionInputPorts(definition);
        if (!inputPorts.length) {
          results.set(node.id, studioApplyComponent(node, definition, null));
          unresolved.delete(node.id);
          changed = true;
          continue;
        }
        const portEdges = new Map(inputPorts.map(port => [port.name, []]));
        let invalidTarget = null;
        edges.forEach(edge => {
          const port = studioInputPort(definition, edge.toPort == null ? null : edge.toPort);
          if (!port) invalidTarget ||= String(edge.toPort || "unknown");
          else portEdges.get(port.name).push(edge);
        });
        if (invalidTarget) {
          results.set(node.id, { status: "OPEN", value: null, note: `relationship targets missing ${invalidTarget} input aperture` });
          unresolved.delete(node.id);
          changed = true;
          continue;
        }
        const vacantPort = inputPorts.find(port => portEdges.get(port.name).length === 0);
        if (vacantPort) {
          results.set(node.id, { status: "OPEN", value: null, note: `vacant ${vacantPort.name}:${vacantPort.type} input` });
          unresolved.delete(node.id);
          changed = true;
          continue;
        }
        const crowdedPort = inputPorts.find(port => portEdges.get(port.name).length > 1);
        if (crowdedPort) {
          results.set(node.id, { status: "MANY", value: null, note: `${portEdges.get(crowdedPort.name).length} incoming relationships compete for ${crowdedPort.name}:${crowdedPort.type}` });
          unresolved.delete(node.id);
          changed = true;
          continue;
        }
        const routed = inputPorts.map(port => ({ port, edge: portEdges.get(port.name)[0] }));
        if (routed.some(item => !results.has(item.edge.from))) continue;
        let blocked = null;
        const bundle = {};
        for (const { port, edge } of routed) {
          const sourceResult = results.get(edge.from);
          const sourceNode = studio.nodes.find(item => item.id === edge.from);
          const disposition = studioConnectionDisposition(sourceNode, node, port.name);
          if (disposition.kind === "OPEN_TYPED_ADAPTER") { blocked = { status: "OPEN", value: null, note: disposition.note }; break; }
          if (sourceResult.status !== "ONE") { blocked = { status: sourceResult.status, value: null, note: `upstream ${edge.from} is ${sourceResult.status}` }; break; }
          const transmitted = studioTransmit(sourceResult.value, studioNodeDefinition(sourceNode).outPort, port.type, disposition, sourceResult.exactValue || null);
          if (transmitted.status !== "ONE") { blocked = { status: transmitted.status, value: null, note: disposition.note }; break; }
          bundle[port.name] = { value: transmitted.value, exactValue: transmitted.exactValue || null, sourceNodeId: sourceNode.id };
        }
        if (blocked) results.set(node.id, blocked);
        else if (inputPorts.length === 1) {
          const only = bundle[inputPorts[0].name];
          const applied = studioApplyComponent(node, definition, only.value);
          if (applied.status === "ONE" && only.exactValue && applied.exactValue == null && definition.id === "trace-receiver") applied.exactValue = only.exactValue;
          results.set(node.id, applied);
        } else results.set(node.id, studioApplyComponent(node, definition, bundle));
        unresolved.delete(node.id);
        changed = true;
      }
    }
    unresolved.forEach(id => results.set(id, { status: "OPEN", value: null, note: "directed cycle requires a separately declared state/update carrier" }));
    studio.nodes.forEach(node => {
      const result = results.get(node.id);
      diagnostics.push({ kind: "NODE", id: node.id, name: node.name, status: result.status, detail: result.note });
    });
    studio.edges.forEach(edge => {
      const source = studio.nodes.find(node => node.id === edge.from);
      const target = studio.nodes.find(node => node.id === edge.to);
      const targetPort = target ? studioInputPort(studioNodeDefinition(target), edge.toPort == null ? null : edge.toPort) : null;
      const disposition = source && target ? studioConnectionDisposition(source, target, targetPort?.name || edge.toPort || null) : { kind: "OPEN_TYPED_ADAPTER", note: "endpoint missing" };
      diagnostics.push({ kind: "EDGE", id: edge.id, name: `${source?.name || edge.from} → ${target?.name || edge.to}${targetPort ? `:${targetPort.name}` : ""}`, status: disposition.kind, detail: disposition.note });
    });
    const statuses = [...results.values()].map(result => result.status);
    const disposition = statuses.includes("NONE") ? "NONE" : statuses.includes("MANY") ? "MANY" : statuses.includes("OPEN") ? "OPEN" : "ONE";
    const terminalIds = studio.nodes.filter(node => !studio.edges.some(edge => edge.from === node.id)).map(node => node.id);
    return { disposition, results, diagnostics, terminalIds };
  }

  function zipD(d, n = state.zip.n) {
    return mod(d + n, 2 * n);
  }
  function require(condition, message) {
    if (!condition) throw new TypeError(message);
  }
  function finite(value, name) {
    require(typeof value === "number" && Number.isFinite(value), name + " must be a finite number");
    return value;
  }
  function record(value, keys, name) {
    require(value !== null && typeof value === "object" && !Array.isArray(value), name + " must be an object");
    require(Object.keys(value).every(key => keys.includes(key)), name + " contains an unsupported field");
  }
  function identifier(value, name) {
    require(typeof value === "string" && value.length > 0 && value.length <= 160, name + " must be a nonempty bounded string");
    return value;
  }
  function carrierN(value) {
    require(Number.isSafeInteger(value) && value >= 1 && value <= 1000000, "carrierN must be an integer in 1..1000000");
    return value;
  }
  function cleanSnapshot(input) {
    record(input, ["schema","intervalTurns","nodes","edges","carrierN","point","selectedNodeIds"], "Graph snapshot");
    require(input.schema === "rprm-motion-graph/v1", "Unknown graph schema");
    require(Array.isArray(input.nodes) && input.nodes.length <= 128, "Graph needs at most 128 nodes");
    require(Array.isArray(input.edges) && input.edges.length <= 512, "Graph needs at most 512 edges");
    const interval = input.intervalTurns === undefined ? [0,32] : input.intervalTurns;
    require(Array.isArray(interval) && interval.length === 2 && interval.every(Number.isFinite) &&
      interval[0] >= 0 && interval[0] < interval[1] && interval[1] <= 32, "Finite increasing turns interval must lie in [0,32]");
    const n=carrierN(input.carrierN === undefined ? 5 : input.carrierN);
    const point=input.point === undefined ? 5 : input.point;
    require(Number.isSafeInteger(point) && point >= 1 && point <= 9, "Point must be an integer in 1..9");
    const nodes=input.nodes.map(node => {
      record(node,["id","componentId","name","aperture","frozenParameters"],"Node");
      const id=identifier(node.id,"Node ID"), componentId=identifier(node.componentId,"Component ID");
      const aperture=node.aperture === undefined ? 0.45 : finite(node.aperture,"Aperture");
      require(aperture>=0 && aperture<=1,"Aperture must lie in [0,1]");
      const name=node.name === undefined ? componentId : identifier(node.name,"Node name");
      const result={id,componentId,name,aperture};
      if(node.frozenParameters !== undefined){record(node.frozenParameters,["n"],"Frozen parameters");result.frozenParameters={n:carrierN(node.frozenParameters.n)};}
      return result;
    });
    require(new Set(nodes.map(node=>node.id)).size===nodes.length,"Duplicate node ID");
    const edges=input.edges.map(edge=>{
      record(edge,["id","from","to","toPort"],"Edge");
      const result={id:identifier(edge.id,"Edge ID"),from:identifier(edge.from,"Edge source"),to:identifier(edge.to,"Edge target")};
      if(edge.toPort !== undefined && edge.toPort !== null) result.toPort=identifier(edge.toPort,"Target port");
      else result.toPort=null;
      return result;
    });
    require(new Set(edges.map(edge=>edge.id)).size===edges.length,"Duplicate edge ID");
    const selected=input.selectedNodeIds === undefined ? [] : input.selectedNodeIds;
    require(Array.isArray(selected) && selected.every(id=>typeof id==="string" && nodes.some(node=>node.id===id)) && new Set(selected).size===selected.length,"Invalid selected node IDs");
    return {schema:"rprm-motion-graph/v1",intervalTurns:interval.slice(),nodes,edges,carrierN:n,point,selectedNodeIds:selected.slice()};
  }
  function sample(id,theta,aperture,receiver="output") {
    require(typeof id==="string" && byId.has(id),"Unknown mechanism");
    finite(theta,"Phase");finite(aperture,"Aperture");
    require(aperture>=0 && aperture<=1,"Aperture must lie in [0,1]");
    require(["output","hidden","typed"].includes(receiver),"Unknown receiver");
    const mechanism=byId.get(id);
    const value=receiver==="typed" ? studioMechanismOutput(id,theta,aperture) : mechanism[receiver](theta,aperture);
    require((Array.isArray(value)?value:[value]).every(Number.isFinite),"Non-finite numeric branch");
    return value;
  }
  function definitions() {
    return studioCoreComponents().map(definition=>({...definition,inputPorts:studioDefinitionInputPorts(definition)}));
  }
  function evaluateGraph(snapshot,turns) {
    const graph=cleanSnapshot(snapshot);
    const [lo,hi]=graph.intervalTurns;
    if(typeof turns!=="number" || !Number.isFinite(turns) || turns<lo || turns>hi) return {
      disposition:"OPEN",nodes:Object.fromEntries(graph.nodes.map(node=>[node.id,{status:"OPEN",value:null,note:"OPEN_NEW_CARRIER: outside declared finite turns interval"}])),
      diagnostics:[],terminalIds:[],intervalTurns:graph.intervalTurns
    };
    state={zip:{n:graph.carrierN},studio:{nodes:graph.nodes,edges:graph.edges,phase:turns,coordinateZipper:{point:graph.point},importedModules:[]}};
    try {
      const evaluated=studioEvaluation();
      // An edge that cannot join the declared graph is still an open obligation,
      // even when a source node independently has one value.
      const openEdge=evaluated.diagnostics.some(item=>item.kind==="EDGE" && item.status==="OPEN_TYPED_ADAPTER");
      const disposition=openEdge && evaluated.disposition==="ONE" ? "OPEN" : evaluated.disposition;
      return {disposition,nodes:Object.fromEntries(evaluated.results),diagnostics:evaluated.diagnostics,terminalIds:evaluated.terminalIds,intervalTurns:graph.intervalTurns};
    } finally { state=undefined; }
  }
  const publicMechanisms=mechanisms.map(({output,hidden,...metadata})=>Object.freeze(metadata));
  return Object.freeze({mechanisms:Object.freeze(publicMechanisms),sample,definitions,evaluateGraph,cleanSnapshot});
})();
