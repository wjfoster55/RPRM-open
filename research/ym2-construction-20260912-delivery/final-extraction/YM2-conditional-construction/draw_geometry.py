"""Static exact-domain illustration and proved-interval comparison; no simulation."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

HERE=Path(__file__).resolve().parent
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':12,'svg.hashsalt':'ym2-joint-construction-20260912'})
fig=plt.figure(figsize=(16,9),facecolor='#f5f3ed')
fig.text(.045,.936,'The joint is required — and the estimate now reaches farther',fontsize=24,weight='bold',color='#15333b')
fig.text(.045,.892,'Two adjacent squares expose the missing relation. Gauge constraints control the full correction on larger lattices.',fontsize=13,color='#45616a')

ax=fig.add_axes([.04,.43,.27,.36]);ax.set_xlim(-.25,2.3);ax.set_ylim(-.5,1.65);ax.axis('off')
ax.text(-.2,1.55,'Two angles leave a relative orientation',fontsize=14,weight='bold',color='#15333b')
ax.add_patch(Rectangle((0,0),1,1,facecolor='#d4e8e4',edgecolor='#147d80',linewidth=3))
ax.add_patch(Rectangle((1,0),1,1,facecolor='#eedbcb',edgecolor='#b56f3f',linewidth=3))
ax.plot([1,1],[0,1],color='#3c5060',linewidth=6)
ax.plot([-.09,2.09,2.09,-.09,-.09],[-.09,-.09,1.09,1.09,-.09],color='#72509a',linewidth=2,linestyle='--')
ax.text(.5,.55,'a',fontsize=27,ha='center',color='#147d80');ax.text(1.5,.55,'b',fontsize=27,ha='center',color='#b56f3f')
ax.text(1,-.29,'c measures the combined outer loop',ha='center',color='#72509a',fontsize=12)
ax.text(1,1.21,'shared link',ha='center',fontsize=11,color='#3c5060')

bx=fig.add_axes([.335,.385,.32,.43],projection='3d',facecolor='#f5f3ed')
s=np.linspace(-1,1,55);aa,bb=np.meshgrid(s,s)
half=np.sqrt(np.maximum(0,(1-aa**2)*(1-bb**2)))
for zz,col in [(aa*bb+half,'#42a4a3'),(aa*bb-half,'#b9a0ce')]:
    bx.plot_surface(aa,bb,zz,color=col,alpha=.43,linewidth=0,antialiased=True,rstride=2,cstride=2)
bx.plot([0,0],[0,0],[-1,1],color='#a14f23',linewidth=3)
bx.scatter([0,0],[0,0],[-1,1],color='#a14f23',s=30)
bx.set_xlabel('a',labelpad=-4);bx.set_ylabel('b',labelpad=-4);bx.set_zlabel('c',labelpad=-4)
bx.set_xticks([-1,0,1]);bx.set_yticks([-1,0,1]);bx.set_zticks([-1,0,1]);bx.tick_params(labelsize=9,pad=0)
bx.view_init(elev=22,azim=-48);bx.set_box_aspect((1,1,1))
fig.text(.365,.8,'The complete two-square joint body',fontsize=14,weight='bold',color='#15333b')
fig.text(.36,.34,'At a = b = 0, every c from −1 to 1 is allowed.',fontsize=11,color='#45616a')

cx=fig.add_axes([.715,.49,.24,.235],facecolor='#f5f3ed')
cx.barh([1,0],[9/128,1/3],height=.48,color=['#b0b6b9','#147d80'])
cx.set_yticks([1,0],['Previous','New']);cx.set_xlim(0,.37);cx.set_xticks([0,.1,.2,1/3],['0','0.1','0.2','1/3'])
cx.set_xlabel('Dimensionless coupling × incidence: mr',fontsize=10)
cx.spines[['top','right']].set_visible(False);cx.grid(axis='x',alpha=.2);cx.set_axisbelow(True)
cx.text(9/128+.008,1,'9/128',va='center',fontsize=11)
cx.text(1/3-.018,0,'1/3',va='center',ha='right',fontsize=11,color='white',weight='bold')
fig.text(.69,.8,'A 4.74× larger proved interval',fontsize=14,weight='bold',color='#15333b')
fig.text(.7,.385,'Actual vacuum + uniform physical gap\nFor d = 3: r ≤ 1/12, gap / E_el ≥ 0.1289',fontsize=11,color='#45616a')

fig.text(.045,.275,'What made the improvement possible',fontsize=17,weight='bold',color='#15333b')
for x,title,body in [(.045,'GAUGE BALANCE','Supported spins reduce the\nquadratic estimate: 16/9 → 1/3.'),
                     (.375,'FIRST OVERLAP CORRECTION','Retain the generated outer-loop term,\nthen prove convergence of the whole tail.'),
                     (.705,'COLLECTIVE CONTROL','The actual response stays below 1\nfor every admitted lattice size.')]:
    fig.text(x,.21,title,fontsize=11,weight='bold',color='#147d80')
    fig.text(x,.155,body,fontsize=12,color='#304d58',linespacing=1.5)
fig.text(.045,.053,'The curved body is exact for the two-square gauge quotient. The bars compare sufficient lattice bounds, not physical phase transitions.',fontsize=10,color='#53646c')
fig.text(.045,.025,'The continuum direction remains open: in the retained convention r = 8/g_b⁴ grows without bound as bare coupling tends to zero.',fontsize=10,color='#53646c')
fig.savefig(HERE/'joint_construction.png',dpi=200,facecolor=fig.get_facecolor())
fig.savefig(HERE/'joint_construction.svg',facecolor=fig.get_facecolor(),metadata={'Date':'2026-09-12'})
print('Saved 3200 x 1800 PNG and SVG')
