\\ Exact rank-zero controls for period and twist scale, independent of BSD.
print("BEGIN_ANCHOR_CONTROL");
M=msinit(32,2,1);H=mscuspidal(M);v=H[1][,1];v=v/(4*mseval(M,v,[oo,0]));
Mp=mspadicinit(M,5,7,0);
roots=polrootspadic(x^2+2*x+5,5,12);al=if(valuation(roots[1],5)==0,roots[1],roots[2]);
L1=mspadicL(mspadicmoments(Mp,v,1),[0,0]);
L8=mspadicL(mspadicmoments(Mp,v,8),[0,0]);
print("base_control=",L1/(1-1/al)^2);
print("raw_twist8_control=",L8/(1+1/al)^2);
print("minimal_E2_component_control=",L8/(2*(1+1/al)^2));
if(valuation(L1/(1-1/al)^2-1/4,5)<7,error("base anchor mismatch"));
if(valuation(L8/(2*(1+1/al)^2)-1/2,5)<7,error("twist period mismatch"));
print("END_ANCHOR_CONTROL");
quit;
