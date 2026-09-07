/* Offline checks of the public kernel, typed graph evaluator and generated Python. */
"use strict";
const fs=require("node:fs"), path=require("node:path"), crypto=require("node:crypto");
const {execFileSync}=require("node:child_process");
const root=path.resolve(__dirname,"../..");
require(path.join(root,"atlas/kernel.js"));
require(path.join(root,"atlas/math-export.js"));
const K=globalThis.MMAKernel,E=globalThis.MMAMathExport,TAU=2*Math.PI;
let assertions=0;
function check(condition,message){assertions++;if(!condition)throw new Error(message);}
function near(a,b,message,tolerance=2e-11){check(Number.isFinite(a)&&Number.isFinite(b)&&Math.abs(a-b)<=tolerance*Math.max(1,Math.abs(a),Math.abs(b)),message);}
function reject(fn,message){let rejected=false;try{fn();}catch{rejected=true;}check(rejected,message);}
function node(id,componentId,aperture=.45,extra={}){return {id,componentId,aperture,...extra};}
function edge(id,from,to,toPort=null){return {id,from,to,toPort};}
function graph(nodes,edges=[],extra={}){return {schema:"rprm-motion-graph/v1",intervalTurns:[0,32],nodes,edges,...extra};}
const apertures=[0,.03125,1/3-1e-10,1/3,.45,2/3-1e-10,2/3,1];
const turns=[0,.03125,.08,.12,.125,.24,.25,.5,.6666666666666666,.91,1,1.5,2,7.125,31.875,32];
check(K.mechanisms.length===20,"Exactly twenty mechanism laws");
check(K.definitions().length===38,"Exactly thirty-eight typed components");
check(new Set(K.definitions().map(d=>d.id)).size===38,"Unique component definitions");

// Mathematical constraints computed separately from the kernel's functions.
for(const a of apertures)for(const t of turns){
  const u=t*TAU;
  for(const m of K.mechanisms)for(const receiver of ["output","hidden","typed"]){
    const value=K.sample(m.id,u,a,receiver);
    check((Array.isArray(value)?value:[value]).every(Number.isFinite),"Finite admitted sample");
  }
  near(K.sample("schmidt",u,a,"typed"),u,"Identity typed phase");
  near(K.sample("schmidt",u,a),Math.sin(u),"Distinct sine display");
  near(K.sample("cv",u,a,"typed"),u,"CV ideal phase");
  near(K.sample("bevel",u,a,"typed"),-(.5+1.5*a)*u,"Bevel ratio");
  near(K.sample("chain",u,a,"typed"),(.55+1.45*a)*u,"Chain ratio");
  near(K.sample("belt",u,a,"typed"),K.sample("chain",u,a,"typed"),"Matching no-slip ratio");
  near(K.sample("gearbox",u,a,"typed"),-[.5,1,2][Math.min(2,Math.floor(3*a))]*u,"Selected gearbox branch");
  near(K.sample("worm",u,a,"typed"),-u/Math.floor(12+48*a+.5),"Worm integer ratio");
  near(K.sample("rack",u,a,"typed"),(.18+.32*a)*u,"Rack pitch law");
  near(K.sample("winch",u,a,"typed"),K.sample("rack",u,a,"typed"),"Constant-radius travel");
  near(K.sample("scotch",u,a,"typed"),(.22+.28*a)*K.sample("scotch",u,a),"Scotch typed radius retained");
  const x=K.sample("slider",u,a,"typed"),rod=2.2+2.8*a;
  near((x-Math.cos(u))**2+Math.sin(u)**2,rod**2,"Slider rod constraint");
  const p=K.sample("chebyshev",u,a,"typed"),ax=Math.cos(u),ay=Math.sin(u),bx=(p[0]+ax)/2,by=(p[1]+ay)/2;
  near(Math.hypot(bx-ax,by-ay),2.5,"First Chebyshev rod");
  near(Math.hypot(bx-2,by),2.5,"Second Chebyshev rod");
  near(p[0],K.sample("chebyshev",u,a),"Path x display");
  near(p[1]-4,K.sample("chebyshev",u,a,"hidden"),"Path paired display offset");
  const phi=K.sample("universal",u,a,"typed"),beta=(8+52*a)*Math.PI/180;
  near(Math.sin(phi)*Math.cos(u),Math.cos(beta)*Math.sin(u)*Math.cos(phi),"Cardan trigonometric constraint");
  near(K.sample("universal",u+TAU,a,"typed"),phi+TAU,"Cardan retained turn");
  for(const id of ["offset","intermittent"]){
    near(K.sample(id,u,a,"typed"),TAU*K.sample(id,u,a),"Gated output units");
    near(K.sample(id,u+TAU,a)-K.sample(id,u,a),1,"Gated next-turn accumulation");
  }
  const gain=.35+1.15*a;
  near(K.sample("one-way",-u,a,"typed"),-K.sample("one-way",u,a,"typed"),"Oriented integral is odd");
  near(K.sample("one-way",u+Math.PI,a,"typed")-K.sample("one-way",u,a,"typed"),2*gain,"Absolute cosine integral period");
  check(Math.abs(K.sample("oscillator",u,a,"typed"))<=.25+.75*a+1e-12,"Oscillator amplitude");
  check(K.sample("cam",u,a,"typed")>=0 && K.sample("cam",u,a,"typed")<=.2+.7*a+1e-12,"Chosen cam bounds");
}

const cases=[];
for(const a of apertures){
  const nodes=[node("motor","motor"),...K.mechanisms.map(m=>node(m.id,m.id,a))];
  cases.push(graph(nodes,K.mechanisms.map(m=>edge("e-"+m.id,"motor",m.id))));
}
for(const kinds of [
  ["motor","bevel","worm","rack","trace-receiver"],
  ["clock","belt","universal","offset","one-way","schmidt","trace-receiver"],
  ["motor","chebyshev","trace-receiver"],
  ["motor","gearbox","limiter","oscillator","intermittent","trace-receiver"],
  ["address-clock","zip-carrier","trace-receiver"]
]){
  const nodes=kinds.map((kind,i)=>node("n"+i,kind,[0,1,.23,.78][i%4],{frozenParameters:{n:7}}));
  cases.push(graph(nodes,nodes.slice(1).map((n,i)=>edge("e"+i,nodes[i].id,n.id))));
}
const carry=graph([node("d","digit-clock"),node("c","carry-one"),node("cell","carry-cell"),node("r","carry-digit-fold"),node("q","carry-out-fold"),node("t","trace-receiver")],
  [edge("d-cell","d","cell","digit"),edge("c-cell","c","cell","carry"),edge("r","cell","r"),edge("q","cell","q"),edge("q-t","q","t")]);
cases.push(carry);
for(let digit=0;digit<=9;digit++){
  const result=K.evaluateGraph(carry,(digit+.25)/10),pair=result.nodes.cell.value;
  check(result.disposition==="ONE","Carry graph closes");
  near(pair[0]+10*pair[1],digit+1,"Carry conservation");
  check(pair[0]>=0&&pair[0]<=9&&[0,1].includes(pair[1]),"Carry output carrier");
}
for(const point of [1,2,3,4,5,6,7,8,9])for(const handoff of [3,5,7]){
  cases.push(graph([node("p","odd-path-clock"),node("l","zip-chart-"+(handoff-1)),node("r","zip-chart-"+(handoff+1)),node("h","zip-handoff-"+handoff)],
    [edge("p-l","p","l"),edge("p-r","p","r"),edge("l-h","l","h","left"),edge("r-h","r","h","right")],{point}));
}
const hostile=[
  graph([node("x","bevel")]),
  graph([node("a","motor"),node("b","motor"),node("x","bevel")],[edge("a-x","a","x"),edge("b-x","b","x")]),
  graph([node("a","bevel"),node("b","belt")],[edge("a-b","a","b"),edge("b-a","b","a")]),
  graph([node("x","bevel")],[edge("ghost","absent","x")]),
  graph([node("m","motor"),node("x","bevel")],[edge("bad","m","x","wrong")]),
  graph([node("m","motor"),node("r","rack"),node("b","bevel")],[edge("m-r","m","r"),edge("r-b","r","b")]),
  graph([node("x","unknown")]),
  graph([]),
  graph([node("m","motor")],[edge("missing-target","m","absent")]),
  graph([node("a","motor"),node("b","motor")],[edge("to-source","a","b")])
];
cases.push(...hostile);
check(K.evaluateGraph(hostile[0],0).disposition==="OPEN","Vacant graph");
check(K.evaluateGraph(hostile[1],0).disposition==="MANY","Competing edge graph");
check(K.evaluateGraph(hostile[2],0).disposition==="OPEN","Cycle graph");
check(K.evaluateGraph(hostile[6],0).nodes.x.status==="OPEN","Unknown component stays open");
check(K.evaluateGraph(hostile[7],0).disposition==="ONE","Empty graph gives empty assignment");
check(K.evaluateGraph(hostile[8],0).disposition==="OPEN","Dangling edge remains open");
check(K.evaluateGraph(hostile[9],0).disposition==="OPEN","Edge into source remains open");
cases.push(graph([node("id_%&#{}","motor",.5,{name:"quote ' \" \\ %_&$#{} ^~ π"})]));

for(const invalid of [NaN,Infinity,-Infinity,true,"0",null]){
  reject(()=>K.sample("bevel",invalid,.5),"Invalid sample phase rejected");
  reject(()=>K.sample("bevel",0,invalid),"Invalid aperture type rejected");
  check(K.evaluateGraph(carry,invalid).disposition==="OPEN","Invalid graph time remains open");
}
for(const invalid of [-1,1.01])reject(()=>K.sample("bevel",0,invalid),"Out-of-domain aperture rejected");
reject(()=>K.sample("missing",0,.5),"Missing mechanism rejected");
reject(()=>K.sample("bevel",0,.5,"unknown"),"Missing receiver rejected");
for(const invalid of [
  {},{...carry,schema:"unknown"},{...carry,privatePayload:"must not persist"},
  {...carry,intervalTurns:[0,Infinity]},{...carry,intervalTurns:[-1,1]},{...carry,intervalTurns:[1,1]},
  {...carry,carrierN:true},{...carry,carrierN:0},{...carry,point:true},{...carry,point:10},
  graph([node("a","motor",true)]),graph([node("a","motor"),node("a","clock")]),
  graph([node("a","motor",.5,{runtime:{code:"never import"}})]),
  graph([node("a","motor")],[edge("e","a","a"),edge("e","a","a")])
]){reject(()=>K.cleanSnapshot(invalid),"Malformed snapshot rejected");reject(()=>E.python(invalid),"Malformed export rejected");}
const definitions=K.definitions(),description=E.describe(graph(definitions.map(d=>node(d.id,d.id))));
definitions.forEach((d,i)=>{check(description.nodes[i].supported,"Every core definition exports");check(JSON.stringify(description.nodes[i].inputPorts)===JSON.stringify(d.inputPorts),"Matching input port types");check(description.nodes[i].outPort===d.outPort,"Matching output port types");});
const before=JSON.stringify(carry),clean=K.cleanSnapshot(carry);
K.evaluateGraph(carry,.5);E.describe(carry);E.python(carry);E.latex(carry);
check(JSON.stringify(carry)===before,"Evaluation and export do not mutate graph input");
clean.nodes[0].aperture=.9;
check(carry.nodes[0].aperture===.45,"Clean snapshot does not alias input nodes");
const escaped=E.latex(cases.at(-1));
for(const token of ["\\textbackslash{}","\\%","\\_","\\&","\\end{document}"])check(escaped.includes(token),"LaTeX escapes retained labels");

const payload=cases.map(snapshot=>({code:E.python(snapshot),snapshot:K.cleanSnapshot(snapshot),reference:turns.map(t=>K.evaluateGraph(snapshot,t))}));
const python=String.raw`
import json, math, sys
data=json.load(sys.stdin)
checked=0
for case in data['cases']:
    namespace={'__name__':'verified_export'}
    exec(compile(case['code'],'composition.py','exec'),namespace)
    assert namespace['SOURCE_SNAPSHOT']==case['snapshot']
    for time,reference in zip(data['turns'],case['reference']):
        actual=namespace['evaluate'](time)
        assert actual['disposition']==reference['disposition'],(time,actual,reference)
        assert actual['terminalIds']==reference['terminalIds']
        assert set(actual['nodes'])==set(reference['nodes'])
        for key,expected in reference['nodes'].items():
            got=actual['nodes'][key]
            assert got['status']==expected['status'],(key,time,got,expected)
            if expected['value'] is None:
                assert got['value'] is None
            else:
                a=got['value'] if isinstance(got['value'],list) else [got['value']]
                b=expected['value'] if isinstance(expected['value'],list) else [expected['value']]
                assert len(a)==len(b)
                assert all(math.isclose(x,y,rel_tol=2e-11,abs_tol=2e-11) for x,y in zip(a,b)),(key,time,a,b)
            checked+=1
    for outside in (-1,33,float('inf'),float('nan'),'0',True,False,None):
        result=namespace['evaluate'](outside)
        assert result['disposition']=='OPEN'
        assert all(x['value'] is None for x in result['nodes'].values())
        checked+=1
    for kind in data['mechanisms']:
        for u,a in ((True,.5),(1,True),(1,False),(1,float('inf'))):
            try: namespace['mechanism'](kind,u,a)
            except ValueError: pass
            else: raise AssertionError(('invalid number accepted',kind,u,a))
            checked+=1
print(json.dumps({'status':'PASS','checks':checked,'graphs':len(data['cases'])}))
`;
const result=JSON.parse(execFileSync(process.env.RPRM_PYTHON||"python",["-I","-B","-c",python],{
  input:JSON.stringify({cases:payload,turns,mechanisms:K.mechanisms.map(m=>m.id)}),encoding:"utf8",maxBuffer:8*1024*1024,timeout:60000
}));
check(result.status==="PASS","Generated Python conformance passes");
const args=process.argv.slice(2);
if(args.length!==2||args[0]!=="--output"||!path.isAbsolute(args[1]))throw new Error("Usage: node checks/atlas/verify.js --output <absolute JSON path>");
const files=["atlas/kernel.js","atlas/math-export.js","checks/atlas/verify.js"];
const report={schema:"rprm-motion-conformance/v1",status:"PASS",javascriptAssertions:assertions,python:result,
  scope:"Finite IEEE-754 ideal-law constraints; 20 display/hidden/typed laws, 38 component definitions, typed graphs, source/receiver distinctions, invalid input controls and generated standard-library Python comparison. No inverse solver, physical dynamics or unbounded result.",
  sourceHashes:Object.fromEntries(files.map(file=>[file,crypto.createHash("sha256").update(fs.readFileSync(path.join(root,file))).digest("hex")]))};
fs.mkdirSync(path.dirname(args[1]),{recursive:true});fs.writeFileSync(args[1],JSON.stringify(report,null,2)+"\n");
process.stdout.write(JSON.stringify(report)+"\n");
