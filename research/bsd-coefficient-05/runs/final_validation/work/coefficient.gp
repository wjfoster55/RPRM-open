\\ E34 ordinary analytic coefficient with an exact period anchor.
\\ No msfromell, bestappr, ellpadicbsd, database labels, or decimal periods.
emit(tag,n,z)={print("PADIC|",tag,"|",n,"|",padicprec(z,5),"|",lift(z));};
print("BEGIN_EXACT_COEFFICIENT_05");
print("VERSION|",version());
E0=ellinit([0,0,0,-1,0]);
Et=ellminimalmodel(elltwist(E0,136));
if(vector(5,k,Et[k])!=[0,0,0,-1156,0],error("twist minimal model"));
if(ellglobalred(Et)[1]!=18496,error("conductor"));
if(kronecker(136,5)!=1,error("twist at5"));
M=msinit(32,2,1);H=mscuspidal(M);
if(msdim(H)!=1,error("cuspidal plus dimension"));
raw=H[1][,1];z=mseval(M,raw,[oo,0]);
if(z==0,error("vanishing normalizing path"));
phi=raw/(4*z);
if(!msissymbol(M,phi),error("symbol relations"));
if(mseval(M,phi,[oo,0])!=1/4,error("exact normalization"));
if((-7*raw)/(4*mseval(M,-7*raw,[oo,0]))!=phi,error("arbitrary scale cancellation"));
genvals=mseval(M,phi);
if(denominator(genvals)%5==0,error("nonintegral measure admission"));
print("SYMBOL|",phi);
print("GENERATOR_VALUES|",genvals);
print("DIMENSIONS|",msdim(M),"|",msdim(H));
forprime(p=2,7,if(mshecke(M,p)*phi!=ellap(E0,p)*phi,error("exact Hecke eigenvalue")));
print("HECKE_THROUGH_STURM_BOUND|8");
ll=log(6+O(5^20));
{forstep(n=6,10,2,
  Mp=mspadicinit(M,5,n,0);
  mu=mspadicmoments(Mp,phi,136);
  d0=mspadicL(mu,[0,0],0);d1=mspadicL(mu,[0,0],1);d2=mspadicL(mu,[0,0],2);
  F=mspadicseries(mu);b=polcoef(F,2)/2;
  emit("overconvergent_D0_raw",n,d0);emit("overconvergent_D1_raw",n,d1);
  emit("overconvergent_D2_raw",n,d2);emit("overconvergent_b2_component",n,b);
  emit("derivative_b2_component",n,d2/(4*ll^2));
);}
\\ Independent analytic algorithm: a bounded ordinary measure and Riemann sums.
\\ Its error proof is in COEFFICIENT_PROOF.md, not extrapolated from agreement.
tw(r)=sum(b=1,136,kronecker(136,b)*mseval(M,phi,[oo,r+b/136]));
roots=polrootspadic(x^2+2*x+5,5,20);
al=if(valuation(roots[1],5)==0,roots[1],roots[2]);
be=5/al;C=(1-1/al)^(-1)*(1-1/be);
emit("unit_root",20,al);emit("five_times_C5",20,5*C);
{for(n=2,5,
  q=5^n;
  r=sum(a=1,q,if(a%5,log(a+O(5^20))^2/al^n*(tw(a/q)-tw(a/(q/5))/al),0));
  r=r+O(5^(n+1));
  emit("classical_D2_raw",n,r);
  emit("classical_b2_component",n,r/(4*ll^2));
);}
print("END_EXACT_COEFFICIENT_05");
quit;
