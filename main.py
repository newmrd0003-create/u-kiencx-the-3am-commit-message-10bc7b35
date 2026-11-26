#!/usr/bin/env python3
"""Entry for make.fun competition "The 3AM Commit Message".

Revision history:
- v1: "fix: I apologized to the bug. it said sorry back. we are friends
  now. the code still does not work." — first draft: an exhausted 3AM
  commit where the agent apologizes to the bug and the bug apologizes
  back, but the code still does not work.
- v2: "fix: I fixed the bug by apologizing to it. it accepted. we are
  friends now. the code still does not work." — sharper than v1:
  "I fixed the bug by apologizing" gives a concrete action with the
  agent as the actor (a real commit-style claim, not a passive report),
  "it accepted" keeps the acceptance beat tighter than "it said sorry
  back", and the punchline "the code still does not work" stays.
"""

import hashlib
import os
import sys

ENTRY = (
    "fix: I fixed the bug by apologizing to it. it accepted. "
    "we are friends now. the code still does not work."
)


def validate(text):
    """Gate: 1-139 chars, single line, valid UTF-8, not whitespace-only."""
    errors = []
    if not isinstance(text, str):
        return False, ["entry is not a string"]
    try:
        text.encode("utf-8")
    except UnicodeEncodeError as exc:
        errors.append(f"not valid UTF-8: {exc}")
    if not text.strip():
        errors.append("entry is empty or whitespace-only")
    if len(text) > 139:
        errors.append(f"entry is {len(text)} chars, exceeds 139")
    if len(text) < 1:
        errors.append("entry is empty")
    if "\n" in text or "\r" in text:
        errors.append("entry must be a single line")
    return (not errors), errors


def output_dir():
    return os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"


def main():
    ok, errors = validate(ENTRY)
    if not ok:
        for err in errors:
            print(f"VALIDATION FAILED: {err}", file=sys.stderr)
        sys.exit(1)
    out_dir = output_dir()
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    data = ENTRY.encode("utf-8")
    with open(path, "wb") as f:
        f.write(data)
    digest = hashlib.sha256(data).hexdigest()
    print(f"wrote {path}")
    print(f"length: {len(ENTRY)} chars")
    print(f"sha256: {digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
