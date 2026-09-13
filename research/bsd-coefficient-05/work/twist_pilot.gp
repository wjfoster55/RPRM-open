\\ Fresh analytic derivative through the conductor32 quadratic twist.
\\ GP ordinary p-adic L, not ellpadicbsd or any assumed rank/Sha formula.
print("BEGIN_TWIST_PILOT");
print(version());
E0=ellinit([0,0,0,-1,0]);
Et=ellminimalmodel(elltwist(E0,136));
print("twisted_minimal_model=",vector(5,k,Et[k]));
print("twisted_conductor=",ellglobalred(Et)[1]);
print("a5=",ellap(Et,5));
print("BEGIN_DERIVATIVE");
gettime();
D2=ellpadicL(E0,5,5,[0,0],2,136);
print("D2=",D2);
print("elapsed_ms=",gettime());
print("END_TWIST_PILOT");
quit;
