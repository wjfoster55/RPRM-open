"""Replay-only F1 pair check against saved F2 rows (not a panel rerun)."""
import argparse, json, sys
from pathlib import Path

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--rows', type=Path, required=True)
    args = ap.parse_args()
    by = {}
    for line in args.rows.read_text(encoding='utf-8').splitlines():
        r = json.loads(line)
        by[r['id']] = r
    tall, flat = by['f1_tall'], by['f1_flat']
    checks = [
        (tall['Q_ref'], 1, 'tall Q'),
        (tall['first_breach'], 11, 'tall first'),
        (tall.get('f1_full_peak'), 22, 'tall peak'),
        (flat['Q_ref'], 0, 'flat Q'),
        (flat['first_breach'], -1, 'flat first'),
        (flat.get('f1_full_peak'), 0, 'flat peak'),
    ]
    bad = [name for got, exp, name in checks if got != exp]
    if bad:
        print({'status': 'FAIL', 'bad': bad})
        sys.exit(1)
    print(json.dumps({'status': 'PASS', 'tall': 1, 'flat': 0, 'peak_tall': 22}))

if __name__ == '__main__':
    main()
