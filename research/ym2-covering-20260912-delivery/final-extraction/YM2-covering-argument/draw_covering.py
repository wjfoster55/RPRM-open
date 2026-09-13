"""Draw exact certificate curves; this is not a spectrum simulation.

Matplotlib is needed only to regenerate the figure. The mathematical
checkers and portable proof do not depend on it.
"""
from pathlib import Path
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch

HERE = Path(__file__).resolve().parent
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':12,
                     'axes.spines.top':False,'axes.spines.right':False,
                     'svg.fonttype':'none'})
fig, axes = plt.subplots(1,3,figsize=(16,7.5),dpi=200,
                         gridspec_kw={'width_ratios':[1,1.15,1.15]})
fig.patch.set_facecolor('#fafbf9')
ink, blue, green, amber = '#1d343d','#276c9e','#28765e','#b76c21'
fig.suptitle('A cover for every collective excitation',x=.055,y=.96,
             ha='left',fontsize=24,color=ink,weight='bold')
fig.text(.055,.90,'Exact bounds for the interacting SU(2) lattice — no spin cutoff, no spectrum sampling',
         fontsize=12,color=ink)

ax=axes[0]
ax.set_title('1  Keep the shared joint',loc='left',pad=22,weight='bold',color=ink)
for x in (0,1):
    ax.add_patch(Rectangle((x,0),1,1,facecolor='#e2edf0',edgecolor=blue,lw=2))
ax.plot([1,1],[0,1],color=amber,lw=6,zorder=3)
for x in (0,1,2):
    for y in (0,1): ax.plot(x,y,'o',color=ink,ms=7,zorder=4)
ax.text(.5,.5,'loop p',ha='center',color=ink)
ax.text(1.5,.5,'loop q',ha='center',color=ink)
ax.annotate('One link variable\nused by both loops',xy=(1,.85),xytext=(1,1.55),
            ha='center',fontsize=12,color=amber,
            arrowprops={'arrowstyle':'->','color':amber,'lw':1.8})
ax.text(1,-.35,'The norm counts every Fourier term\ntouching each link, including large supports.',
        ha='center',va='top',fontsize=11,color=ink,linespacing=1.6)
ax.text(1,-1.1,'All physical states sit inside the full\nlink space with the same ground state.\nAn ambient lower bound covers them all.',
        ha='center',va='top',fontsize=11,color=ink,linespacing=1.6)
ax.set(xlim=(-.3,2.3),ylim=(-2.1,2));ax.axis('off')

ax=axes[1]
ax.set_title('2  Bound the vacuum bending',loc='left',pad=22,weight='bold',color=ink)
x=[i/400 for i in range(451)]
Y=[3/8*(1-math.sqrt(max(0,1-8*s/9))) for s in x]
gap=[1-2*y for y in Y]
ax.axvspan(0,1,color='#e4f2e9',zorder=0)
ax.plot(x,gap,color=green,lw=3,label='Certified gap / electric energy unit')
ax.plot(x,Y,color=blue,lw=2,label='Upper bound on log-vacuum norm')
ax.scatter([1,1],[.5,.25],color=[green,blue],zorder=5)
ax.axvline(1,ls='--',color=green,lw=1.2)
ax.axvline(1.125,ls=':',color=amber,lw=2)
ax.text(.98,.69,'Safe endpoint\ngap ≥ 1/2',ha='right',color=green,fontsize=11)
ax.scatter([1.125],[.25],facecolors='#fafbf9',edgecolors=green,zorder=6)
ax.scatter([1.125],[.375],facecolors='#fafbf9',edgecolors=blue,zorder=6)
ax.annotate('Contraction ends here;\nlimiting gap bound is 1/4',xy=(1.125,.25),
            xytext=(.10,.36),fontsize=10,color=amber,
            arrowprops={'arrowstyle':'->','color':amber})
ax.set(xlim=(0,1.18),ylim=(0,1.05),xlabel='Interaction ratio / safe threshold',ylabel='Dimensionless bound')
ax.set_xticks([0,.5,1,1.125],['0','0.5','1','9/8'])
ax.grid(alpha=.15)
ax.legend(loc='upper right',fontsize=8,frameon=False,bbox_to_anchor=(1,.96))

ax=axes[2]
ax.set_title('3  Separate the two limits',loc='left',pad=22,weight='bold',color=ink)
ax.axvspan(0,1,color='#dcefe4')
ax.axvspan(1,2.5,color='#f0efec')
ax.axvline(1,ls='--',color=green,lw=2)
ax.text(.5,2.1,'PROVED\nFOR EVERY\nFINITE SIZE',ha='center',va='center',
        color=green,weight='bold',fontsize=13,linespacing=1.6)
ax.text(1.77,2.1,'Outside the\nheadline certificate\n\nActual gap unresolved\nby this bound',
        ha='center',va='center',color='#626a6e',fontsize=11,linespacing=1.5)
ax.add_patch(FancyArrowPatch((.48,3.15),(.48,3.9),arrowstyle='->',mutation_scale=18,color=green,lw=2))
ax.text(.52,3.65,'more cells',color=green,fontsize=10,rotation=90,va='center')
ax.add_patch(FancyArrowPatch((.45,.5),(2.2,.5),arrowstyle='->',mutation_scale=18,color=amber,lw=2))
ax.text(1.32,.68,'Continuum tuning changes the ratio',ha='center',color=amber,fontsize=9)
ax.set(xlim=(0,2.5),ylim=(0,4),xlabel='Magnetic / electric ratio, relative to safe bound',
       ylabel='Finite lattice size (schematic)')
ax.set_xticks([0,1,2],['0','1','2']);ax.set_yticks([])

fig.text(.055,.055,'Safe threshold: r ≤ 1/96 in two spatial dimensions; r ≤ 1/192 in three.  '
         'This is a fixed-lattice result; continuum existence and mass-gap survival remain open.',
         fontsize=10,color=ink)
fig.subplots_adjust(left=.055,right=.97,bottom=.17,top=.80,wspace=.40)
fig.savefig(HERE/'covering_argument.png',facecolor=fig.get_facecolor())
fig.savefig(HERE/'covering_argument.svg',facecolor=fig.get_facecolor())
print('Wrote 3200 x 1500 PNG and editable SVG.')
