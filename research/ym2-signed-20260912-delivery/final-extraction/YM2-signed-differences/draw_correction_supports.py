"""Render the exact support structure used in the gauge-averaged heat bound.

Optional figure reproduction requires existing matplotlib; no simulation.
The three research checkers use only the standard library.
"""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
POINTS = {'A':(0,0),'B':(1,0),'C':(2,0),'D':(0,1),'E':(1,1),'F':(2,1)}
EDGES = {'a':('A','B'),'b':('B','C'),'c':('D','E'),'d':('E','F'),
         'l':('A','D'),'s':('B','E'),'r':('C','F')}
NAVY, MUTED, BLUE, RED, LIGHT = '#172c42','#52677a','#007f89','#bb4b48','#d8e0e7'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':13,
                     'svg.fonttype':'none','savefig.facecolor':'#fafbfd'})

def graph(ax, support, color=BLUE, leaves=(), labels=False):
    for edge,(a,b) in EDGES.items():
        x1,y1=POINTS[a]
        x2,y2=POINTS[b]
        enabled=edge in support
        ax.plot([x1,x2],[y1,y2],color=color if enabled else LIGHT,
                lw=5 if enabled else 1.7,solid_capstyle='round',
                zorder=2 if enabled else 1)
    for name,(x,y) in POINTS.items():
        active=any(name in EDGES[e] for e in support)
        ax.scatter([x],[y],s=112 if name in leaves else 64,
                   color='#fafbfd' if name in leaves else (color if active else LIGHT),
                   edgecolors=color if name in leaves else '#fafbfd',
                   linewidths=2.3 if name in leaves else 1.1,zorder=3)
        if labels:
            ax.text(x,y+(0.15 if y else -0.19),name,ha='center',va='center',
                    color=RED if name in leaves else MUTED,fontsize=11)
    ax.set_xlim(-.28,2.28)
    ax.set_ylim(-.35,1.35)
    ax.set_aspect('equal')
    ax.axis('off')

fig=plt.figure(figsize=(13,9),facecolor='#fafbfd')
fig.text(.065,.95,'Subtract the reference. Join the corrections.',
         color=NAVY,fontsize=23,weight='bold')
fig.text(.065,.90,r'$q_s=1+r_s,\qquad \int r_s\,d\mu=0,\qquad |r_s|\leq d$',
         color=MUTED,fontsize=17)

left=fig.add_axes([.06,.53,.40,.29])
right=fig.add_axes([.54,.53,.40,.29])
graph(left,{'a','l','c'},RED,leaves=('B','E'),labels=True)
graph(right,{'a','l','c','s'},BLUE,labels=True)
fig.text(.26,.825,'Open correction chain',ha='center',color=NAVY,fontsize=17,weight='bold')
fig.text(.74,.825,'Closed correction loop',ha='center',color=NAVY,fontsize=17,weight='bold')
fig.text(.26,.508,'An open end has only one correction factor.',ha='center',color=MUTED,fontsize=11.5)
fig.text(.26,.466,'Gauge average: zero',ha='center',color=RED,fontsize=17,weight='bold')
fig.text(.74,.508,'Correction factors meet at every active vertex.',ha='center',color=MUTED,fontsize=11.5)
fig.text(.74,.466,r'May survive: magnitude $\leq d^4$',ha='center',color=BLUE,fontsize=17,weight='bold')

fig.text(.065,.398,'All four possible nonempty supports after cancellation',
         color=NAVY,fontsize=16,weight='bold')
supports=[({'a','l','c','s'},r'Left cell: $d^4$'),
          ({'b','r','d','s'},r'Right cell: $d^4$'),
          ({'a','l','c','d','r','b'},r'Outer loop: $d^6$'),
          (set(EDGES),r'All seven links: $d^7$')]
for i,(support,label) in enumerate(supports):
    ax=fig.add_axes([.06+.235*i,.20,.215,.17])
    graph(ax,support)
    fig.text(.1675+.235*i,.185,label,ha='center',color=NAVY,fontsize=13)
fig.text(.5,.105,r'$|K_{\mathrm{phys},s}-1|\ \leq\ 2d^4+d^6+d^7$',
         ha='center',color=BLUE,fontsize=23)
fig.text(.5,.042,'Exact two-cell SU(2) support structure. These are heat-kernel correction terms, not field trajectories.',
         ha='center',color=MUTED,fontsize=10.5)
fig.savefig(HERE/'correction_supports.png',dpi=160)
fig.savefig(HERE/'correction_supports.svg')
plt.close(fig)
print('Rendered correction_supports.png and correction_supports.svg')
