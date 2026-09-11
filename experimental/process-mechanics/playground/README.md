# Process-mechanics offline playground

Three local views:

1. **Continuation** — same rank display, different successor; color is sufficient.
2. **Join** — same-participant filter versus a false cross-candidate mix.
3. **Reuse** — context mismatch rejects cached reasons.

Open `index.html` in a browser. No network after download.

Automated `check.py` tests the pure `model.js` via Node. Browser UI review is
**NOT_RUN** unless separately executed.

## Manual browser smoke checklist

- [ ] Page loads offline
- [ ] Seed slider updates continuation JSON
- [ ] Join toggle flips EMPTY_FAMILY vs RESOLVED
- [ ] Plan change rejects reuse
- [ ] Reset restores seed 10
- [ ] Export JSON marks `NEW_ILLUSTRATIVE_DEMO` and sandbox edit
- [ ] Keyboard: Ctrl/Cmd+R resets (page handler)

Edits are sandbox experiments, not paper revalidation.
