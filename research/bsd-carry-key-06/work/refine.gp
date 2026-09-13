\\ Same exact anchor and independent measure formula as experiment 05.
emit(tag,n,z)={print("PADIC|",tag,"|",n,"|",padicprec(z,5),"|",lift(z));};
print("BEGIN_CARRY_KEY_06");
print("VERSION|",version());
E0=ellinit([0,0,0,-1,0]);
Et=ellminimalmodel(elltwist(E0,136));
if(vector(5,k,Et[k])!=[0,0,0,-1156,0],error("twist minimal model"));
if(kronecker(136,5)!=1,error("twist at5"));
M=msinit(32,2,1);H=mscuspidal(M);
if(msdim(H)!=1,error("cuspidal plus dimension"));
raw=H[1][,1];z=mseval(M,raw,[oo,0]);
if(z==0,error("vanishing anchor"));
phi=raw/(4*z);
if(!msissymbol(M,phi),error("symbol relations"));
if(mseval(M,phi,[oo,0])!=1/4,error("exact normalization"));
if(denominator(mseval(M,phi))%5==0,error("measure integrality"));
forprime(p=2,7,if(mshecke(M,p)*phi!=ellap(E0,p)*phi,error("Hecke eigenvalue")));
ll=log(6+O(5^20));
Mp=mspadicinit(M,5,8,0);mu=mspadicmoments(Mp,phi,136);
bc=polcoef(mspadicseries(mu),2)/2;
emit("overconvergent_b2",8,bc);
lm=log(-4+O(5^20));cu=lm/ll;
if(valuation(lm+ll-log(1-25+O(5^20)),5)<20,error("log product identity"));
if(valuation(lm+ll,5)!=2 || valuation(lm-ll,5)!=1,error("log sum/difference valuations"));
emit("coordinate_unit",20,cu);
emit("transported_coefficient",8,bc/cu^2);
tw(r)=sum(b=1,136,kronecker(136,b)*mseval(M,phi,[oo,r+b/136]));
roots=polrootspadic(x^2+2*x+5,5,20);
al=if(valuation(roots[1],5)==0,roots[1],roots[2]);
{for(n=4,6,
  q=5^n;
  r=sum(a=1,q,if(a%5,log(a+O(5^20))^2/al^n*(tw(a/q)-tw(a/(q/5))/al),0));
  r=r+O(5^(n+1));
  emit("classical_D2_raw",n,r);
  emit("classical_b2",n,r/(4*ll^2));
);}
print("END_CARRY_KEY_06");
quit;
