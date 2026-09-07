/* Portable Studio laws. No DOM, imported-code execution, or display normalization.
 * Generated Python uses only the standard library on the declared interval. */
globalThis.MMAMathExport = (() => {
  "use strict";
  const rule = (inPort, outPort, formula, latex) => ({inPort, outPort, formula, latex});
  const R = {
    motor: rule(null, "rotary.phase", "y = 2πt", String.raw`y=2\pi t`),
    clock: rule(null, "time.turns", "y = t", "y=t"),
    "digit-clock": rule(null, "digit.base10", "y = floor(10 frac(t))", String.raw`y=\lfloor10\operatorname{frac}(t)\rfloor`),
    "carry-one": rule(null, "carry.bit", "y = 1", "y=1"),
    "address-clock": rule(null, "strong.address", "y = floor(2n frac(t))", String.raw`y=\lfloor2n\operatorname{frac}(t)\rfloor`),
    "zip-carrier": rule("strong.address", "strong.address", "y = (round_JS(u)+n) mod 2n", String.raw`y=(\lfloor u+1/2\rfloor+n)\bmod 2n`),
    "carry-cell": {...rule("digit.base10 + carry.bit", "digit-carry.base10", "y = [r,q]; q=floor((d+c)/10), r=d+c−10q", String.raw`q=\lfloor(d+c)/10\rfloor,\quad y=(d+c-10q,q)`), inputPorts: [{name:"digit",type:"digit.base10"},{name:"carry",type:"carry.bit"}]},
    "carry-digit-fold": rule("digit-carry.base10", "digit.base10", "y = [r,q][0] = r", "y=r"),
    "carry-out-fold": rule("digit-carry.base10", "carry.bit", "y = [r,q][1] = q", "y=q"),
    "trace-receiver": rule("receiver.any", "receipt.trace", "y = u (retain incoming type on edge)", "y=u"),
    "odd-path-clock": rule(null, "absolute.address", "y = retained path point", String.raw`y=x_{\mathrm{retained}}`),
    schmidt: rule("rotary.phase", "rotary.phase", "y = u", "y=u"),
    cv: rule("rotary.phase", "rotary.phase", "y = u", "y=u"),
    universal: rule("rotary.phase", "rotary.phase", "β=(8+52a)π/180; k=floor((u+π)/(2π)); v=u−2πk; y=atan2(cos(β)sin(v),cos(v))+2πk", String.raw`\begin{aligned}\beta&=(8+52a)\pi/180,\\ k&=\lfloor(u+\pi)/(2\pi)\rfloor,\quad v=u-2\pi k,\\y&=\operatorname{atan2}(\cos\beta\sin v,\cos v)+2\pi k\end{aligned}`),
    bevel: rule("rotary.phase", "rotary.phase", "y = −(0.5+1.5a)u", "y=-(0.5+1.5a)u"),
    slider: rule("rotary.phase", "linear.position", "L=2.2+2.8a; y=cos(u)+sqrt(max(0,L²−sin²(u)))", String.raw`L=2.2+2.8a,\quad y=\cos u+\sqrt{\max(0,L^2-\sin^2u)}`),
    "sun-planet": rule("rotary.phase", "linear.position", "y = cos(u/2)", String.raw`y=\cos(u/2)`),
    scotch: rule("rotary.phase", "linear.position", "y = (0.22+0.28a)cos(u)", String.raw`y=(0.22+0.28a)\cos u`),
    chebyshev: rule("rotary.phase", "path.xy", "A=(cos(u),sin(u)); O=(2,0); D=|O−A|; H=sqrt(max(0,2.5²−D²/4)); B=(A+O)/2+H(−(O−A)y,(O−A)x)/D; y=2B−A", String.raw`\begin{aligned}A&=(\cos u,\sin u),\quad O=(2,0),\\D&=\lVert O-A\rVert,\quad H=\sqrt{\max(0,2.5^2-D^2/4)},\\B&=(A+O)/2+H(-(O-A)_y,(O-A)_x)/D,\\y&=2B-A\end{aligned}`),
    chain: rule("rotary.phase", "rotary.phase", "y = (0.55+1.45a)u", "y=(0.55+1.45a)u"),
    belt: rule("rotary.phase", "rotary.phase", "y = (0.55+1.45a)u", "y=(0.55+1.45a)u"),
    gearbox: rule("rotary.phase", "rotary.phase", "j=min(2,floor(3a)); y=−[0.5,1,2][j]u", String.raw`j=\min(2,\lfloor3a\rfloor),\quad y=-r_j u,\quad(r_0,r_1,r_2)=(0.5,1,2)`),
    oscillator: rule("rotary.phase", "rotary.phase", "y = (0.25+0.75a)(2/π)asin(sin(u))", String.raw`y=(0.25+0.75a)\frac2\pi\arcsin(\sin u)`),
    limiter: rule("rotary.phase", "rotary.phase", "y = u min(1,1/(0.45+1.45a))", String.raw`y=u\min(1,(0.45+1.45a)^{-1})`),
    winch: rule("rotary.phase", "length.unwrapped", "y = (0.18+0.32a)u", "y=(0.18+0.32a)u"),
    rack: rule("rotary.phase", "linear.position", "y = (0.18+0.32a)u", "y=(0.18+0.32a)u"),
    offset: rule("rotary.phase", "rotary.phase", "y = 2π G(u;0.12,0.12+0.43a)", String.raw`y=2\pi G(u;0.12,0.12+0.43a)`),
    "one-way": rule("rotary.phase", "rotary.unwrapped", "y=(0.35+1.15a) I(u); I(u)=integral from 0 to u of |cos(v)| dv", String.raw`y=(0.35+1.15a)I(u),\quad I(u)=\int_0^u|\cos v|\,dv`),
    cam: rule("rotary.phase", "linear.position", "y = (0.20+0.70a)max(0,cos(u))²", String.raw`y=(0.20+0.70a)\max(0,\cos u)^2`),
    intermittent: rule("rotary.phase", "rotary.phase", "y = 2π G(u;0.08,0.10+0.32a)", String.raw`y=2\pi G(u;0.08,0.10+0.32a)`),
    worm: rule("rotary.phase", "rotary.phase", "y = −u/floor(12+48a+0.5)", String.raw`y=-u/\lfloor12+48a+0.5\rfloor`)
  };
  for (const c of [2,4,6,8]) R[`zip-chart-${c}`] = rule("absolute.address", "chart.coordinate", `x=round_JS(u); y=x−${c} when |x−${c}|≤1; otherwise OPEN`, String.raw`x=\lfloor u+1/2\rfloor,\quad y=x-${c}\quad\text{if }|x-${c}|\le1`);
  for (const p of [3,5,7]) R[`zip-handoff-${p}`] = {...rule("left + right chart coordinates", "handoff.receipt", `y=${p} only for (left,right)=(1,−1); otherwise OPEN`, String.raw`y=${p}\quad\text{if }(u_{\mathrm{left}},u_{\mathrm{right}})=(1,-1)`), inputPorts:[{name:"left",type:"chart.coordinate"},{name:"right",type:"chart.coordinate"}]};
  const ADAPTERS = Object.freeze({"rotary.unwrapped→rotary.phase":"ADAPTER", "rotary.phase→rotary.unwrapped":"ADAPTER", "length.unwrapped→linear.position":"ADAPTER", "linear.position→length.unwrapped":"ADAPTER", "time.turns→rotary.phase":"ADAPTER", "path.1d→linear.position":"ADAPTER", "path.2d→path.xy":"CAR", "path.2d→linear.position":"FOLD", "path.3d→path.xy":"FOLD"});
  const copy = value => JSON.parse(JSON.stringify(value));
  const textEscape = value => String(value).replace(/[\\{}$&#%_^~]/g, ch => ({"\\":"\\textbackslash{}","{":"\\{","}":"\\}","$":"\\$","&":"\\&","#":"\\#","%":"\\%","_":"\\_","^":"\\textasciicircum{}","~":"\\textasciitilde{}"}[ch])).replace(/[\r\n]+/g," ");
  function unpack(snapshot) {
    const graph=globalThis.MMAKernel.cleanSnapshot(snapshot);
    return {studio:{graph:{nodes:graph.nodes,edges:graph.edges},importedModules:[],selectedNodeIds:graph.selectedNodeIds,coordinateHandoffZipper:{point:graph.point}},interval:graph.intervalTurns};
  }
  function ports(definition) {
    if (Array.isArray(definition?.inputPorts) && definition.inputPorts.length) return definition.inputPorts.map(p => ({name:String(p.name),type:String(p.type)}));
    return definition?.inPort ? [{name:"in",type:definition.inPort}] : [];
  }
  function describe(snapshot) {
    snapshot=globalThis.MMAKernel.cleanSnapshot(snapshot);
    const {studio,interval} = unpack(snapshot);
    const imported = new Map((studio.importedModules || []).map(module => [module.id,module]));
    const selected = new Set(studio.selectedNodeIds || [studio.selectedNodeId]);
    const unsupported = [];
    const nodes = studio.graph.nodes.map(node => {
      const core = Object.hasOwn(R,node.componentId) ? R[node.componentId] : null;
      const definition = core || imported.get(node.componentId);
      const supported = Boolean(core);
      const reason = supported ? null : definition ? "Imported/custom operation retained; portable execution is not registered." : "Missing component definition.";
      if (reason) unsupported.push({id:node.id,component:node.componentId,reason});
      const n = Number.isInteger(node.frozenParameters?.n) ? node.frozenParameters.n : snapshot.carrierN;
      const parameters = {aperture:node.aperture};
      if (["address-clock","zip-carrier"].includes(node.componentId)) parameters.n = n;
      if (node.componentId === "odd-path-clock") parameters.point = studio.coordinateHandoffZipper?.point;
      const scope = supported ? `Studio typed output on t ∈ [${interval.join(", ")}] turns; rotary input u is radians; a=${node.aperture}. Forward evaluation only. Geometry, forces and inverse fibers are not computed; the admitted graph JSON retains the evaluation inputs.` : reason;
      return {id:node.id,name:node.name || node.componentId,component:node.componentId,formula:core?.formula || "OPEN_UNSUPPORTED — no portable equation registered",latex:core?.latex || String.raw`\mathrm{OPEN}_{\mathrm{UNSUPPORTED}}`,scope,supported,inPort:definition?.inPort || null,outPort:definition?.outPort || null,inputPorts:ports(definition),parameters,selected:selected.has(node.id)};
    });
    const byId = new Map(nodes.map(node => [node.id,node]));
    const connections = studio.graph.edges.map(edge => {
      const from = byId.get(edge.from), to = byId.get(edge.to);
      const target = to?.inputPorts.find(port => edge.toPort == null || port.name === edge.toPort);
      const sourceType = from?.outPort || null, targetType = target?.type || null;
      const disposition = !sourceType || !targetType ? "OPEN_TYPED_ADAPTER" : targetType === "receiver.any" ? "FOLD" : sourceType === targetType ? "EXACT" : ADAPTERS[`${sourceType}→${targetType}`] || "OPEN_TYPED_ADAPTER";
      const operation = disposition === "OPEN_TYPED_ADAPTER" ? "OPEN: no declared typed bridge" : sourceType === "time.turns" && targetType === "rotary.phase" ? "u = 2π y_source" : ["path.2d","path.3d"].includes(sourceType) && ["path.xy","linear.position"].includes(targetType) ? targetType === "path.xy" ? "u = first two coordinates" : "u = first coordinate" : "u = y_source";
      return {...copy(edge),sourceType,targetType,targetPort:target?.name || edge.toPort || null,disposition,operation};
    });
    return {schema:"mechanical-motion-math-export/v1",nodes,connections,intervalTurns:interval.slice(),supported:unsupported.length===0,unsupported,summary:`${nodes.length} components, ${connections.length} directed relationships; ${nodes.length-unsupported.length} registered portable laws, ${unsupported.length} unsupported. Entire graph retained. Input interval [${interval.join(", ")}] turns; no display normalization or physical closure is claimed.`};
  }
  function latex(snapshot) {
    const description = describe(snapshot);
    const lines = ["% Compile with LuaLaTeX or XeLaTeX (UTF-8 component names are retained).",String.raw`\documentclass{article}`,String.raw`\usepackage[margin=20mm]{geometry}`,String.raw`\usepackage{fontspec}`,String.raw`\usepackage{amsmath,amssymb}`,String.raw`\setlength{\emergencystretch}{3em}`,String.raw`\begin{document}`,String.raw`\section*{Mechanical composition}`,textEscape(description.summary),String.raw`\par $t$ is input turns, $u$ is a component's transmitted input, $y$ its output, and $a$ its retained aperture. Rotary inputs use radians.`,String.raw`\par $\operatorname{frac}(x)=x-\lfloor x\rfloor$. For the gated laws,`,String.raw`\begin{align*}G(u;s,w)&=\lfloor u/(2\pi)\rfloor+S((\operatorname{frac}(u/(2\pi))-s)/w),\\S(z)&=h^2(3-2h),\quad h=\max(0,\min(1,z)).\end{align*}`,String.raw`\par These are forward ideal Studio laws. Inverse fibers, loads, physical construction, and imported operations remain outside this export. The admitted graph JSON retains the evaluation inputs.`];
    description.nodes.forEach((node,i) => {
      lines.push(String.raw`\subsection*{${i+1}. ${textEscape(node.name)} (${textEscape(node.id)})}`,String.raw`\noindent Component: \texttt{${textEscape(node.component)}}. Ports: \texttt{${textEscape(node.inPort || "SOURCE")}} to \texttt{${textEscape(node.outPort || "OPEN")}}.`,String.raw`\par Parameters: \texttt{${textEscape(JSON.stringify(node.parameters))}}.`,String.raw`\begin{gather*}${node.latex}\end{gather*}`,textEscape(node.scope));
    });
    lines.push(String.raw`\section*{Directed composition}`);
    if (!description.connections.length) lines.push("No directed relationships are retained.");
    description.connections.forEach(edge => lines.push(String.raw`\par \texttt{${textEscape(edge.from)}} $\longrightarrow$ \texttt{${textEscape(edge.to)}}:${textEscape(edge.targetPort || "OPEN")} --- ${textEscape(edge.disposition)}; ${textEscape(edge.operation)}.`));
    lines.push(String.raw`\end{document}`);
    return lines.join("\n")+"\n";
  }
  function python(snapshot) {
    snapshot=globalThis.MMAKernel.cleanSnapshot(snapshot);
    const description = describe(snapshot);
    return `# Mechanical Motion Atlas: finite Studio composition\n# Run: python composition.py [turns]; default is 0 turns.\n# Imported/custom operations remain OPEN_UNSUPPORTED.\n# The admitted graph snapshot is retained below for editable JSON reopening.\nimport json\nimport math\nimport sys\n\nSOURCE_SNAPSHOT = json.loads(${JSON.stringify(JSON.stringify(snapshot))})\nDESCRIPTION = json.loads(${JSON.stringify(JSON.stringify(description))})\n` + PYTHON_RUNTIME;
  }
  const PYTHON_RUNTIME = String.raw`
TAU = 2 * math.pi

def result(status, value=None, note=""):
    return {"status": status, "value": value, "note": note}

def mechanism(kind, u, a):
    if type(a) not in (int, float) or not math.isfinite(a) or not 0 <= a <= 1:
        raise ValueError("aperture outside [0,1]")
    if isinstance(u, list):
        u = u[0]
    if type(u) not in (int, float) or not math.isfinite(u):
        raise ValueError("non-finite mechanism input")
    if kind in ("schmidt", "cv"):
        return u
    if kind == "universal":
        k = math.floor((u + math.pi) / TAU)
        v = u - k * TAU
        return math.atan2(math.cos((8 + 52*a)*math.pi/180)*math.sin(v), math.cos(v)) + k*TAU
    if kind == "bevel":
        return -(0.5 + 1.5*a)*u
    if kind == "slider":
        return math.cos(u) + math.sqrt(max(0, (2.2+2.8*a)**2 - math.sin(u)**2))
    if kind == "sun-planet":
        return math.cos(u/2)
    if kind == "scotch":
        return (0.22 + 0.28*a)*math.cos(u)
    if kind == "chebyshev":
        ax, ay = math.cos(u), math.sin(u)
        dx, dy = 2-ax, -ay
        d = math.hypot(dx, dy)
        h = math.sqrt(max(0, 2.5**2-(d/2)**2))
        bx, by = (ax+2)/2-dy/d*h, ay/2+dx/d*h
        return [2*bx-ax, 2*by-ay]
    if kind in ("chain", "belt"):
        return (0.55+1.45*a)*u
    if kind == "gearbox":
        return -[0.5,1,2][min(2,math.floor(a*3))]*u
    if kind == "oscillator":
        return (0.25+0.75*a)*2/math.pi*math.asin(math.sin(u))
    if kind == "limiter":
        return u*min(1,1/(0.45+1.45*a))
    if kind in ("winch", "rack"):
        return (0.18+0.32*a)*u
    if kind in ("offset", "intermittent"):
        start, width = (0.12,0.12+0.43*a) if kind == "offset" else (0.08,0.10+0.32*a)
        t = u/TAU
        whole = math.floor(t)
        phase = t-whole
        local = 1 if phase >= start+width else 0
        if start < phase < start+width:
            z = max(0,min(1,(phase-start)/width))
            local = z*z*(3-2*z)
        return (whole+local)*TAU
    if kind == "one-way":
        x = abs(u)
        periods = math.floor(x/math.pi)
        rem = x-periods*math.pi
        tail = math.sin(rem) if rem <= math.pi/2 else 2-math.sin(rem)
        return (0.35+1.15*a)*(-1 if u < 0 else 1)*(2*periods+tail)
    if kind == "cam":
        return (0.20+0.70*a)*max(0,math.cos(u))**2
    if kind == "worm":
        return -u/math.floor(12+48*a+0.5)
    raise ValueError("unknown portable mechanism")

def apply(node, inputs, turns):
    kind = node["component"]
    if not node["supported"]:
        return result("OPEN", note="OPEN_UNSUPPORTED: " + node["scope"])
    p = node["parameters"]
    u = inputs
    try:
        if kind == "motor":
            y = turns*TAU
        elif kind == "clock":
            y = turns
        elif kind == "digit-clock":
            y = math.floor((turns-math.floor(turns))*10)
        elif kind == "carry-one":
            y = 1
        elif kind in ("address-clock", "zip-carrier"):
            n = p.get("n")
            if type(n) is not int or n < 1:
                return result("OPEN", note="Missing positive integer strong carrier n")
            y = math.floor((turns-math.floor(turns))*2*n) if kind == "address-clock" else (math.floor(u+0.5)+n) % (2*n)
        elif kind == "carry-cell":
            d, c = u["digit"], u["carry"]
            if type(d) not in (int,float) or type(c) not in (int,float) or d != math.floor(d) or not 0 <= d <= 9 or c not in (0,1):
                return result("NONE", note="Carry domain requires d in 0..9, c in {0,1}")
            q, r = divmod(d+c,10)
            y = [r,q]
        elif kind in ("carry-digit-fold", "carry-out-fold"):
            if not isinstance(u,list) or len(u) != 2 or any(type(v) not in (int,float) or v != math.floor(v) for v in u):
                return result("NONE", note="Projection requires retained integer pair")
            y = u[0 if kind == "carry-digit-fold" else 1]
        elif kind == "odd-path-clock":
            y = p.get("point")
            if type(y) is not int or not 1 <= y <= 9:
                return result("OPEN", note="Missing retained path point in 1..9")
        elif kind.startswith("zip-chart-"):
            c, x = int(kind.rsplit("-",1)[1]), math.floor(u+0.5)
            if abs(x-c) > 1:
                return result("OPEN", note="Outside retained coordinate chart")
            y = x-c
        elif kind.startswith("zip-handoff-"):
            if (u["left"],u["right"]) != (1,-1):
                return result("OPEN", note="Handoff requires (+1,-1) paired chart receipts")
            y = int(kind.rsplit("-",1)[1])
        elif kind == "trace-receiver":
            y = u
        else:
            a = p.get("aperture")
            if type(a) not in (int,float) or not math.isfinite(a) or not 0 <= a <= 1:
                return result("NONE", note="Aperture outside retained [0,1] domain")
            y = mechanism(kind,u,a)
        vector = y if isinstance(y,list) else [y]
        if not all(type(v) in (int,float) and math.isfinite(v) for v in vector):
            return result("NONE", note="Non-finite exported numeric branch")
        return result("ONE",y,"Forward Studio typed output")
    except (ArithmeticError, ValueError, TypeError, KeyError, IndexError) as error:
        return result("NONE",note="Numeric branch: " + str(error))

def evaluate(turns):
    """Return disposition, nodes (status/value/note), edges and terminalIds.

    The declared finite interval is inclusive. Unsupported operations, vacant
    inputs, undeclared typed bridges and cycles never acquire numeric values.
    MANY means competing incoming edges, not a solved inverse fiber.
    """
    nodes, edges = DESCRIPTION["nodes"], DESCRIPTION["connections"]
    lo, hi = DESCRIPTION["intervalTurns"]
    if type(turns) not in (int,float) or not math.isfinite(turns) or not lo <= turns <= hi:
        return {"disposition":"OPEN", "nodes":{n["id"]:result("OPEN",note="OPEN_NEW_CARRIER: outside declared finite turns interval") for n in nodes}, "edges":edges, "terminalIds":[], "intervalTurns":[lo,hi]}
    by_id = {n["id"]:n for n in nodes}
    incoming = {n["id"]:[] for n in nodes}
    for edge in edges:
        if edge.get("to") in incoming:
            incoming[edge["to"]].append(edge)
    values, pending = {}, set(by_id)
    changed = True
    while changed:
        changed = False
        for node in nodes:
            nid = node["id"]
            if nid not in pending:
                continue
            input_ports = node["inputPorts"]
            found = incoming[nid]
            out = None
            if not node["supported"]:
                out = apply(node,None,turns)
            elif not input_ports:
                out = apply(node,None,turns)
            else:
                port_edges = {p["name"]:[] for p in input_ports}
                invalid = False
                for edge in found:
                    name = edge.get("targetPort")
                    if name not in port_edges:
                        invalid = True
                    else:
                        port_edges[name].append(edge)
                vacant = next((p for p in input_ports if not port_edges[p["name"]]),None)
                crowded = next((p for p in input_ports if len(port_edges[p["name"]])>1),None)
                if invalid:
                    out = result("OPEN",note="Relationship targets missing input aperture")
                elif vacant:
                    out = result("OPEN",note="Vacant input " + vacant["name"])
                elif crowded:
                    out = result("MANY",note="Competing relationships at " + crowded["name"])
                elif any(port_edges[p["name"]][0]["from"] not in values for p in input_ports):
                    continue
                else:
                    bundle = {}
                    for port in input_ports:
                        edge = port_edges[port["name"]][0]
                        prior = values[edge["from"]]
                        if edge["disposition"] == "OPEN_TYPED_ADAPTER":
                            out = result("OPEN",note="OPEN_TYPED_ADAPTER: no declared typed bridge")
                            break
                        if prior["status"] != "ONE":
                            out = result(prior["status"],note="Upstream " + edge["from"] + " is " + prior["status"])
                            break
                        value = prior["value"]
                        if edge["sourceType"] == "time.turns" and edge["targetType"] == "rotary.phase":
                            value = value*TAU
                        elif isinstance(value,list) and edge["targetType"] in ("linear.position","path.xy"):
                            value = value[:2] if edge["targetType"] == "path.xy" else value[0]
                        bundle[port["name"]] = value
                    if out is None:
                        out = apply(node,bundle[input_ports[0]["name"]] if len(input_ports)==1 else bundle,turns)
            values[nid] = out
            pending.remove(nid)
            changed = True
    for nid in pending:
        values[nid] = result("OPEN",note="Directed cycle or missing endpoint requires a declared state/update carrier")
    statuses = {r["status"] for r in values.values()}
    disposition = next((s for s in ("NONE","MANY","OPEN") if s in statuses),"ONE")
    if disposition == "ONE" and any(e["disposition"] == "OPEN_TYPED_ADAPTER" for e in edges):
        disposition = "OPEN"
    return {"disposition":disposition, "nodes":values, "edges":edges, "terminalIds":[n["id"] for n in nodes if not any(e.get("from")==n["id"] for e in edges)], "intervalTurns":[lo,hi]}

if __name__ == "__main__":
    print(json.dumps(evaluate(float(sys.argv[1]) if len(sys.argv)>1 else 0),indent=2,ensure_ascii=False,allow_nan=False))
`;
  return Object.freeze({describe,python,latex});
})();
