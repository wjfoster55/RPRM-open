"""A scale illustration, not a field or spectral simulation."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

HERE=Path(__file__).resolve().parent
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':12,'svg.fonttype':'none'})
fig,axs=plt.subplots(1,3,figsize=(14,6),dpi=200)
fig.patch.set_facecolor('#fbfaf6')
fig.suptitle('Two different ways to get more cells',fontsize=23,x=.055,y=.96,ha='left',weight='bold',color='#253b43')
fig.text(.055,.89,'All three drawings use the same length scale. These lengths are illustrative.',fontsize=12,color='#52606a')
for ax,title,extent,step,color,caption in zip(axs,
    ['Starting description','Extend the region','Refine the same region'],
    [2,4,2],[1,1,.5],['#376f98','#28765e','#ba712a'],
    ['2 m across; each cell is 1 m','4 m across; each cell is still 1 m','Still 2 m across;\neach cell is now 0.5 m']):
    ax.set_title(title,loc='left',fontsize=16,weight='bold',color=color,pad=10)
    n=round(extent/step)
    ax.add_patch(Rectangle((0,0),extent,extent,facecolor=color,alpha=.12))
    for k in range(n+1):
        v=k*step
        ax.plot([v,v],[0,extent],color=color,lw=1.5)
        ax.plot([0,extent],[v,v],color=color,lw=1.5)
    ax.annotate('',xy=(0,-.3),xytext=(extent,-.3),arrowprops={'arrowstyle':'<->','color':color,'lw':1.3})
    ax.text(extent/2,-.48,f'{extent} metres',ha='center',va='top',color=color)
    ax.text(0,-1.10,caption,color=color,fontsize=10)
    ax.set(xlim=(-.15,4.35),ylim=(-1.3,4.25));ax.set_aspect('equal');ax.axis('off')
fig.text(.365,.115,'The all-size bound covers this growth\nat a fixed admitted interaction ratio.',color='#28765e',fontsize=11,linespacing=1.5)
fig.text(.685,.115,'Continuum work also needs a proved relation\nbetween parameters and physical readouts.',color='#ba712a',fontsize=11,linespacing=1.5)
fig.subplots_adjust(left=.055,right=.975,top=.80,bottom=.17,wspace=.10)
fig.savefig(HERE/'scale_changes.png',facecolor=fig.get_facecolor())
fig.savefig(HERE/'scale_changes.svg',facecolor=fig.get_facecolor())
print('Wrote 2800 x 1200 illustration and SVG.')
