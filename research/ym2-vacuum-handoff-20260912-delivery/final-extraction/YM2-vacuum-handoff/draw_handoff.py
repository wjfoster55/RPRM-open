"""Explanatory diagram of exact reference transport; no simulation."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, FancyArrowPatch

HERE=Path(__file__).resolve().parent
plt.rcParams.update({"font.family":"DejaVu Sans","svg.fonttype":"none"})
fig,ax=plt.subplots(figsize=(15,7),facecolor="#f5f3ee")
fig.subplots_adjust(left=0,right=1,bottom=0,top=1)
ax.set_xlim(0,15);ax.set_ylim(0,7);ax.axis("off")
ink="#182f3b";muted="#52656d";teal="#14786c";gold="#be7229"
def text(x,y,s,size=13,**kwargs):
    ax.text(x,y,s,fontsize=size,color=kwargs.pop("color",ink),**kwargs)
def box(x,y,w,h,color="#e6ecea"):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=.12,rounding_size=.13",
                              linewidth=0,facecolor=color))
text(.55,6.50,"A new reference can take over. The correction must come with it.",21,weight="bold")
text(.55,6.08,"Two useful results from the compensator and teacher-handoff ideas",13,color=muted)

text(.65,5.42,"The number connection is exact",16,weight="bold")
text(.65,5.00,"Variance contribution 1.5  :  energy load 1",13)
ax.add_patch(Rectangle((.65,4.15),3.0,.5,color=teal,lw=0))
ax.add_patch(Rectangle((3.65,4.15),2.0,.5,color=gold,lw=0))
text(2.15,4.40,"0.6",16,color="white",ha="center",va="center",weight="bold")
text(4.65,4.40,"0.4",16,color="white",ha="center",va="center",weight="bold")
text(.65,3.76,"Divide both contributions by their sum, 2.5.",12,color=muted)
text(.65,3.21,"Ratio:  0.6 / 0.4 = 1.5",15,weight="bold",color=teal)
text(.65,2.78,"Signed contrast:  −0.6 + 0.4 = −0.2",15,weight="bold")
text(.65,2.29,"These describe the same ratio in different coordinates.",11.5,color=muted)
text(.65,1.96,"They are not a new set of block weights.",11.5,color=muted)

text(7.0,5.42,"The physical state stays the same",16,weight="bold")
box(7.0,4.08,2.40,.80)
box(11.75,4.08,2.40,.80)
text(8.20,4.59,"old reference",12,ha="center")
text(8.20,4.23,r"$\Psi=\phi_a f_a$",17,ha="center")
text(12.95,4.59,"new reference",12,ha="center")
text(12.95,4.23,r"$\Psi=\phi_b f_b$",17,ha="center")
ax.add_patch(FancyArrowPatch((9.6,4.46),(11.53,4.46),arrowstyle="-|>",mutation_scale=16,color=teal,lw=2))
text(10.56,4.97,r"$f_b=(\phi_a/\phi_b)f_a$",14,ha="center",color=teal)
box(7.0,2.77,7.15,.72,"#f1e5d5")
text(10.57,3.13,"Carry: reference motion + residual energy",14,ha="center",va="center",weight="bold")
text(7.0,2.29,"Dropping the residual changes the Hamiltonian.",11.5,color=muted)
text(7.0,1.96,"A calibrated handoff keeps the whole operation.",11.5,color=muted)

ax.plot([.6,14.3],[1.57,1.57],color="#c9d0cc",lw=1)
text(.65,1.04,"CLOSED",12,color=teal,weight="bold")
text(1.65,1.04,"Exact ratio, decoding and operator transport",12)
text(.65,.53,"OPEN",12,color=gold,weight="bold")
text(1.65,.53,"Bound the actual correction at one link AND its combined influence across the field",12)
fig.savefig(HERE/"vacuum_handoff.png",dpi=200,facecolor=fig.get_facecolor())
fig.savefig(HERE/"vacuum_handoff.svg",facecolor=fig.get_facecolor())
plt.close(fig)
