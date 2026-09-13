"""Plot the exact wrapped and lifted trajectories from this experiment."""
import argparse
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--evidence',type=Path,required=True)
    ap.add_argument('--output-dir',type=Path,required=True)
    args=ap.parse_args()
    rows=json.loads(args.evidence.read_text())['carry']['current_path']
    out=args.output_dir;out.mkdir(parents=True,exist_ok=True)
    if (out/'sawtooth_and_lift.png').exists():raise FileExistsError('Use a new figure directory')
    k=[r['k'] for r in rows];F=[r['wrapped'] for r in rows];L=[r['lifted'] for r in rows]
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11})
    fig,axes=plt.subplots(2,1,figsize=(10,7),sharex=True,layout='constrained')
    fig.suptitle('One process, two readouts',fontsize=20,fontweight='bold')
    for ax in axes:
        ax.spines[['top','right']].set_visible(False)
        ax.grid(axis='y',alpha=.2);ax.set_xlim(-.3,20.3)
        ax.axvline(10,color='#718096',linestyle=':',linewidth=1.3)
    axes[0].plot(k,F,color='#176b9b',marker='o',markersize=4,linewidth=2)
    axes[0].axhline(566,color='#718096',linestyle='--',linewidth=.8)
    axes[0].set_title('Wrapped digit display',loc='left',fontweight='bold')
    axes[0].set_ylabel('F(k)');axes[0].set_ylim(0,1220)
    axes[0].annotate('566: the display returns',xy=(10,566),xytext=(11.4,1020),
                     arrowprops={'arrowstyle':'->','color':'#176b9b'},color='#176b9b')
    axes[1].plot(k,L,color='#9b4717',marker='o',markersize=4,linewidth=2)
    axes[1].set_title('Retained wraps added back:  L(k) = F(k) + 10 C(k) = 566 + 121 k',
                      loc='left',fontweight='bold',fontsize=11)
    axes[1].set_ylabel('L(k)');axes[1].set_xlabel('Number of shadow steps k')
    axes[1].annotate('1776: the lift has advanced by 1210',xy=(10,1776),xytext=(1,2660),
                     arrowprops={'arrowstyle':'->','color':'#9b4717'},color='#9b4717')
    axes[1].set_xticks(range(0,21,2))
    fig.savefig(out/'sawtooth_and_lift.png',dpi=160)
    fig.savefig(out/'sawtooth_and_lift.svg')
    plt.close(fig)
    (out/'RENDER.json').write_text(json.dumps({'matplotlib':matplotlib.__version__,
        'source_evidence':str(args.evidence),'scope':'Exact model values, not measured physical data'},indent=2)+'\n')
    print(str((out/'sawtooth_and_lift.png').resolve()))


if __name__=='__main__':main()
