---
title: install.sh — mkdir-then-symlink creates link INSIDE empty dir
track: knowledge
category: best-practices
module: kiro/install.sh
component: install
severity: error
tags: [bash, install, symlink, ln-sfn]
applies_when:
  - install script creates a directory tree first, then symlinks bundle dirs into it
  - the symlink target path is one of the directories `mkdir -p` already created
pattern: |
  `ln -sfn <src> <dst>` only replaces `<dst>` when `<dst>` is a file or an
  existing symlink. If `<dst>` is a real (empty) directory, `ln -sfn` creates
  the symlink as a CHILD of `<dst>` instead of replacing it.

  Two safe patterns:

  1. Skip the mkdir for any path that's about to become a symlink. Walk the
     two lists separately:
     ```bash
     # only mkdir paths that stay as real dirs
     for sub in skills agents agents/prompts settings erpaval erpaval/settings; do
       mkdir -p "${TARGET}/${sub}"
     done
     # then ln -sfn the symlink targets — these paths must NOT be in the mkdir loop
     for spec in "${LINK_SPECS[@]}"; do
       link "${ERPAVAL_BUNDLE}/${spec%%::*}" "${TARGET}/${spec##*::}"
     done
     ```

  2. Defensively rmdir empty dirs before ln -sfn:
     ```bash
     if [[ -d "$dst" && ! -L "$dst" && -z "$(ls -A "$dst" 2>/dev/null)" ]]; then
       rmdir "$dst"
     fi
     ln -sfn "$src" "$dst"
     ```

  Verify with: after install, run `python -c "import os; print(os.path.exists('<expected_path>'))"`.
example_files:
  - kiro/install.sh
---

# Why this matters

Silent failure mode: the installer reports success ("Installed."), but the
hooks resolve to `<target>/erpaval/hooks/kiro_session_start_bootstrap.py`
which doesn't exist because the symlink lives at
`<target>/erpaval/hooks/hooks` instead of replacing the empty `hooks/`
directory. Kiro's hook runner errors at session start with a confusing
"command not found" instead of the script doing useful work.

# Example

```bash
# WRONG — creates the symlink inside the empty dir:
mkdir -p /target/erpaval/hooks
ln -sfn /bundle/hooks /target/erpaval/hooks
# Result: /target/erpaval/hooks/hooks -> /bundle/hooks
ls /target/erpaval/hooks/kiro_session_start_bootstrap.py  # MISSING

# RIGHT — skip the mkdir for symlink targets:
ln -sfn /bundle/hooks /target/erpaval/hooks
# Result: /target/erpaval/hooks -> /bundle/hooks
ls /target/erpaval/hooks/kiro_session_start_bootstrap.py  # OK
```
