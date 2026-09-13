"""Standalone scientific illustration from the proved closed formulas."""
from pathlib import Path
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE=Path(__file__).resolve().parent
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':12,
                     'axes.spines.top':False,'axes.spines.right':False})
fig=plt.figure(figsize=(16,9),facecolor='#f6f8fc')
fig.text(.065,.94,'What the operational refinement keeps',fontsize=27,weight='bold',color='#183047')
fig.text(.065,.895,'A cancellation has components. Each component retains its own response rate and link support.',fontsize=15,color='#41566b')
ax=fig.add_axes([.075,.32,.40,.48],facecolor='white')
t=[k/1500 for k in range(751)]
slow=[3/16*math.exp(-9*x) for x in t]
fast=[-3/16*math.exp(-13*x) for x in t]
ax.plot(t,slow,color='#1b8a9b',lw=2.5,label='Energy-9 component')
ax.plot(t,fast,color='#bd6452',lw=2.5,label='Energy-13 component')
ax.plot(t,[a+b for a,b in zip(slow,fast)],color='#5744a8',lw=3,label='Combined response')
ax.axhline(0,color='#9cabb8',lw=.8)
ax.scatter([0],[0],color='#5744a8',s=65,zorder=5)
ax.set(xlabel='Auxiliary kinetic heat time',ylabel='Response at one admitted SU(2) configuration',xlim=(0,.5),ylim=(-.215,.24))
ax.set_title('Zero now can have a nonzero continuation',loc='left',pad=16,fontsize=16,weight='bold')
ax.legend(loc='upper right',fontsize=10,frameon=False)
ax.annotate('Exactly zero at the start',xy=(0,0),xytext=(.075,-.115),arrowprops={'arrowstyle':'->','color':'#5744a8'},color='#5744a8',fontsize=11)
ax.grid(alpha=.14)
bx=fig.add_axes([.575,.32,.36,.48],facecolor='white')
js=[1+k/2 for k in range(39)]
for z,color in [(1,'#1b8a9b'),(13,'#5744a8'),(50,'#bd6452')]:
    values=[]
    for j in js:
        lm=8*j*j-2;lp=8*j*j+16*j+6
        wm=8*(j+1)*(2*j)**3;wp=8*j*(2*j+2)**3
        values.append((wm*lm/(lm+z)+wp*lp/(lp+z))/(wm+wp))
    bx.plot(js,values,color=color,lw=2.5,label=f'Fixed shift z = {z}')
bx.axhline(1,color='#354758',linestyle='--',lw=1)
bx.annotate('1 = no improvement',xy=(15,1),xytext=(10,.81),
            arrowprops={'arrowstyle':'->','color':'#354758'},fontsize=11,color='#354758')
bx.set(xlabel='Spin j in the exact one-square family',ylabel='Shifted / unshifted anchored response norm',xlim=(1,20),ylim=(.13,1.035))
bx.set_title('The remaining uniform-control problem',loc='left',pad=16,fontsize=16,weight='bold')
bx.legend(loc='lower right',frameon=False,fontsize=10)
bx.grid(alpha=.14)
fig.text(.075,.235,'LEFT  The two rates are 9 and 13. Their sum starts at zero; its integrated response is exactly 1/156.',fontsize=12,color='#354758')
fig.text(.075,.195,'RIGHT  Every fixed positive shift helps low modes, but its relative benefit tends to zero as spin grows.',fontsize=12,color='#354758')
fig.text(.075,.135,'Checked gain: retain the channel’s support before counting its cost at a shared link.',fontsize=15,weight='bold',color='#183047')
fig.text(.075,.09,'The proof improves a finite-coupling lattice gap certificate. These plots are exact-formula illustrations, not a continuum simulation.',fontsize=11,color='#53677a')
for ext in ('png','svg'):fig.savefig(HERE/f'operational_seam.{ext}',dpi=200)
