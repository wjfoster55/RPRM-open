# Publication policy

This repository publishes released papers and reviewed code with the source,
documentation, tests, and build inputs needed to use them. Keep unpublished
research, drafts, chat exports, review bundles, backups, and disposable output
in private working directories outside the checkout. Share only necessary,
reviewed exports; do not nest copies of delivered bundles.

Normal implementation changes belong in their documented repository modules.
Saving or backing up work does not authorize publication. Do not use blanket
add/commit/push autosync as backup. Stage explicit paths and review both the
staged diff and every outgoing commit, including earlier commits containing
files since removed. Check the remote destination before publishing.

## Local guard

Run from the repository root before publishing a commit or branch:

```sh
python -I -B tools/check_publication.py --ref HEAD
```

The read-only guard checks every distinct tree in the selected commit's
reachable history for directories named `research`, `tmp`,
`recovered-concepts`, `experiments`, `RPRM-CORE-FORMALIZATION-01`, `.local`,
or `.claude`, and the directory pair `papers/absolute-distinction`. It also
rejects `.zip`, `.7z`, `.tar`, `.gz`, and `.rar` paths and blobs larger than
100 MiB anywhere in that history. Path matching is case-insensitive. Two
reviewed compressed evidence inputs are allowed only at their exact paths
and Git blob IDs, as recorded in `RELEASE_INPUTS` in the guard:

- `experimental/process-mechanics/public_evidence/pc1/LEARNER_ORIGIN_PREDICTIONS.csv.gz`
  (`2a2bb0e59749de3b63a00eef22eda5baa7d298c7`)
- `experimental/process-mechanics/public_evidence/pc1/OBSERVER_ORIGIN_RECORDS.csv.gz`
  (`e7c9580393e1d17790e50de67534097fa5cd041a`)

Changing either file's content or path requires another publication review;
other `.gz` files are rejected. Deleting a prohibited file in the latest
commit does not remove it from history.
Shallow repositories and refs that do not resolve to commits are rejected.
Submodules are unsupported: every gitlink (tree mode `160000`) in reachable
history is rejected, including gitlinks deleted before the proposed tip.

The optional pre-push hook checks each proposed local ref's actual object ID
and skips deletions. It uses local Git objects and Python 3, without network
access. To enable it in a standalone checkout:

```sh
git config core.hooksPath .githooks
```

Git configuration can be shared by linked worktrees. Check that scope before
enabling the hook; this repository does not configure it automatically.

These are limited path and size checks, not a secret audit or proof that a
release is suitable for publication. Uncommitted files are outside a ref's
history. Ignore rules do not remove tracked files, and an opt-in hook can be
bypassed. Review the contents and outgoing history even when the guard passes.
