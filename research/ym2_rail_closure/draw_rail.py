"""Static explanatory figure; exact four-state values, no physical simulation."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

HERE=Path(__file__).resolve().parent
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':13,
                     'svg.hashsalt':'ym2-rail-closure-20260912'})
fig=plt.figure(figsize=(16,9.5),facecolor='#f6f4ef')
fig.text(.045,.945,'A closed rail needs an energy check',fontsize=26,weight='bold',color='#162e3b')
fig.text(.045,.906,'Consistency recovers a law. The vacuum equation and collective response are additional obligations.',
         fontsize=13,color='#41525a')

ax=fig.add_axes([.045,.47,.43,.38]);ax.set_xlim(0,1);ax.set_ylim(0,1);ax.axis('off')
ax.text(0,1,'1  Two routes must give the same ratio',fontsize=16,weight='bold',color='#162e3b')
positions={'x':(.13,.17),'i':(.82,.17),'j':(.13,.72),'ij':(.82,.72)}
labels={'x':r'$x$', 'i':r'$x^i$', 'j':r'$x^j$', 'ij':r'$x^{ij}$'}
for start,end,col in [('x','i','#007f86'),('i','ij','#007f86'),('x','j','#ae6437'),('j','ij','#ae6437')]:
    ax.add_patch(FancyArrowPatch(positions[start],positions[end],arrowstyle='-|>',
             mutation_scale=18,linewidth=2.8,color=col,shrinkA=22,shrinkB=22))
for name,(x,y) in positions.items():
    ax.scatter([x],[y],s=1050,c='#ffffff',edgecolor='#162e3b',linewidth=1.7,zorder=3)
    ax.text(x,y,labels[name],ha='center',va='center',fontsize=19,zorder=4)
ax.text(.475,.23,'change link i',color='#007f86',ha='center')
ax.text(.475,.78,'change link i',color='#ae6437',ha='center')
ax.text(.17,.45,'change\nlink j',color='#ae6437',va='center')
ax.text(.84,.45,'change\nlink j',color='#007f86',va='center')
ax.text(.48,.47,'same endpoints\nsame density ratio',ha='center',va='center',weight='bold',color='#162e3b')
ax.text(.48,-.02,'If all such rectangles close, the joint law is unique.',ha='center',fontsize=12)

bx=fig.add_axes([.565,.56,.38,.24],facecolor='#f6f4ef')
fig.text(.535,.85,'2  Closure alone does not prevent a slow point',fontsize=16,weight='bold',color='#162e3b')
xs=[0,1,2,3,4];ys=[1,.4,2/17,.4,1]
bx.plot(xs,ys,color='#72529a',linewidth=3,marker='o',markersize=8)
for x,y,t in zip(xs,ys,['1','2/5','2/17','2/5','1']):
    bx.annotate(t,(x,y),xytext=(0,12),textcoords='offset points',ha='center',fontsize=12,weight='bold')
bx.set_ylim(0,1.2);bx.set_yticks([0,.5,1]);bx.set_xticks(xs,['0','log 2','log 4','log 2','0'])
bx.set_xlabel('Reference parameter a — this is not physical time',fontsize=11)
bx.set_ylabel('Exact heat-bath gap',fontsize=11)
bx.spines[['top','right']].set_visible(False);bx.grid(axis='y',alpha=.18)
fig.text(.55,.45,'Four-state control: gap = 1 − tanh(a).\nThe final reference equals the initial reference.',fontsize=12,color='#41525a')

cx=fig.add_axes([.045,.105,.91,.27]);cx.set_xlim(0,1);cx.set_ylim(0,1);cx.axis('off')
cx.text(0,1,'3  Three checks carry the YM claim',fontsize=16,weight='bold',color='#162e3b')
cards=[(.0,'RELATIONAL CONSISTENCY','All update rectangles close','One joint probability law','#dceee8'),
       (.355,'ACTUAL VACUUM','(Aφ)/φ is constant everywhere','The law belongs to this Hamiltonian','#e6e3f1'),
       (.71,'COLLECTIVE CONTROL','Influence contracts uniformly','A positive uniform gap bound','#f0e5ce')]
for left,title,middle,bottom,color in cards:
    cx.add_patch(FancyBboxPatch((left,.22),.285,.58,boxstyle='round,pad=.01,rounding_size=.02',
                              facecolor=color,edgecolor='none'))
    cx.text(left+.1425,.65,title,ha='center',fontsize=11,weight='bold',color='#162e3b')
    cx.text(left+.1425,.49,middle,ha='center',fontsize=11,color='#162e3b')
    cx.text(left+.1425,.33,bottom,ha='center',fontsize=10.5,color='#41525a')
for left in [.29,.645]:
    cx.add_patch(FancyArrowPatch((left,.5),(left+.06,.5),arrowstyle='-|>',mutation_scale=20,
                                color='#5a6b73',linewidth=1.8))
cx.text(.5,.03,'FLICK handoff: valid parent  →  prepare + verify the successor  →  accept against the current revision',
        ha='center',fontsize=12,color='#162e3b')
fig.text(.045,.025,'The rectangle is schematic; the plotted four-state values are exact. This is not a YM simulation or a continuum mass-gap result.',
         fontsize=10,color='#53636b')
fig.savefig(HERE/'rail_closure.png',dpi=200,facecolor=fig.get_facecolor())
fig.savefig(HERE/'rail_closure.svg',facecolor=fig.get_facecolor(),metadata={'Date':'2026-09-12'})
plt.close(fig)
print('Saved 3200 x 1900 PNG and SVG')
