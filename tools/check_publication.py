#!/usr/bin/env python3
"""Check declared publication path/size rules across one local ref's history."""

import argparse
import os
from pathlib import PurePosixPath
import subprocess
import sys


PRIVATE_DIRS = {
    "research", "tmp", "recovered-concepts", "experiments",
    "rprm-core-formalization-01", ".local", ".claude",
}
ARCHIVE_SUFFIXES = {".zip", ".7z", ".tar", ".gz", ".rar"}
MAX_BLOB_BYTES = 100 * 1024 * 1024
# Existing reviewed release inputs: both exact path AND Git blob ID must match.
RELEASE_INPUTS = {
    ("experimental/process-mechanics/public_evidence/pc1/LEARNER_ORIGIN_PREDICTIONS.csv.gz",
     "2a2bb0e59749de3b63a00eef22eda5baa7d298c7"),
    ("experimental/process-mechanics/public_evidence/pc1/OBSERVER_ORIGIN_RECORDS.csv.gz",
     "e7c9580393e1d17790e50de67534097fa5cd041a"),
}


def git(*args, data=None):
    # Inspect local objects only, without replacement histories or lazy fetches.
    env = dict(os.environ, GIT_NO_LAZY_FETCH="1", GIT_OPTIONAL_LOCKS="0")
    result = subprocess.run(
        ["git", "--no-replace-objects", *args], input=data,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env,
    )
    if result.returncode:
        raise RuntimeError(result.stderr.decode("utf-8", "replace").strip())
    return result.stdout


def prohibited(path, oid):
    parts = PurePosixPath(path.casefold()).parts
    directories = parts[:-1]
    return (
        bool(PRIVATE_DIRS.intersection(directories))
        or any(pair == ("papers", "absolute-distinction")
               for pair in zip(directories, directories[1:]))
        or (PurePosixPath(path).suffix.casefold() in ARCHIVE_SUFFIXES
            and (path, oid) not in RELEASE_INPUTS)
    )


def check(ref):
    if git("rev-parse", "--is-shallow-repository").strip() == b"true":
        raise RuntimeError("a shallow repository cannot establish full history")
    commit = git("rev-parse", "--verify", "--end-of-options",
                 ref + "^{commit}").strip().decode("ascii")
    trees = set(git("log", "--format=%T", commit, "--").splitlines())
    rejected_paths = set()
    rejected_gitlinks = set()
    # Every distinct historical tree preserves ALL names for identical blobs,
    # including paths renamed or removed before the proposed tip.
    for tree in sorted(trees):
        entries = git("ls-tree", "-r", "-z", tree.decode("ascii"))
        for entry in entries.split(b"\0"):
            if entry:
                header, raw = entry.split(b"\t", 1)
                mode, _, raw_oid = header.split()
                oid = raw_oid.decode("ascii")
                path = raw.decode("utf-8", "surrogateescape")
                if mode == b"160000":
                    rejected_gitlinks.add(path)
                if prohibited(path, oid):
                    rejected_paths.add(path)
    objects = git("rev-list", "--objects", "--no-object-names", commit, "--")
    sizes = git("cat-file", "--batch-check=%(objectname) %(objecttype) %(objectsize)",
                data=objects)
    oversized = []
    blobs = 0
    for row in sizes.splitlines():
        fields = row.split()
        if len(fields) != 3:
            raise RuntimeError("a reachable object is unavailable locally")
        oid, kind, size = fields
        if kind == b"blob":
            blobs += 1
            if int(size) > MAX_BLOB_BYTES:
                oversized.append((oid.decode("ascii"), int(size)))
    for path in sorted(rejected_paths):
        print(f"REJECT path in history: {path!r}", file=sys.stderr)
    for path in sorted(rejected_gitlinks):
        print(f"REJECT unsupported gitlink in history: {path!r}", file=sys.stderr)
    for oid, size in oversized:
        print(f"REJECT blob {oid}: {size} bytes (>100 MiB)", file=sys.stderr)
    if rejected_paths or rejected_gitlinks or oversized:
        return 1
    print(f"PASS publication rules: {commit} ({len(trees)} trees, {blobs} blobs)")
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ref", default="HEAD", help="local commit or ref (default: HEAD)")
    args = parser.parse_args()
    try:
        return check(args.ref)
    except (OSError, RuntimeError, ValueError) as error:
        print(f"Publication check failed: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
