\\ Independent ordinary-measure Riemann sums from exact classical symbols.
\\ No mspadicinit, mspadicmoments, mspadicL, mspadicseries or msfromell.
print("BEGIN_CLASSICAL_PILOT");
M=msinit(32,2,1);H=mscuspidal(M);raw=H[1][,1];
phi=raw/(4*mseval(M,raw,[oo,0]));
print("generator_values=",mseval(M,phi));
tw(r)=sum(b=1,136,kronecker(136,b)*mseval(M,phi,[oo,r+b/136]));
al=polrootspadic(x^2+2*x+5,5,12);al=if(valuation(al[1],5)==0,al[1],al[2]);
print("unit_root=",al);
for(n=2,4, gettime();q=5^n;v=sum(a=1,q,if(a%5,log(a+O(5^12))^2/al^n*(tw(a/q)-tw(a/(q/5))/al),0));print("n=",n," raw_Riemann=",v+O(5^(n+1))," elapsed_ms=",gettime()));
print("END_CLASSICAL_PILOT");
quit;
