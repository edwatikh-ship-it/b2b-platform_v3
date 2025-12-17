from __future__ import annotations

import re
import sys
from pathlib import Path


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("api-contracts.yaml")
    txt = path.read_text(encoding="utf-8")

    m = re.search(r"(?ms)^paths:\s*\r?\n(.*?)(\r?\n^[^\s].*|\Z)", txt)
    if not m:
        print("ERROR: 'paths:' block not found in " + str(path), file=sys.stderr)
        return 2

    body = m.group(1)

    bad = []
    for i, line in enumerate(body.splitlines(), start=1):
        mm = re.match(r"^(  )([^ \t:#][^:#]*):\s*$", line)
        if not mm:
            continue
        key = mm.group(2).strip()
        if not key.startswith("/"):
            bad.append((i, key))

    if bad:
        print("ERROR: OpenAPI paths keys must start with '/' (file: %s)" % path, file=sys.stderr)
        for lineno, key in bad[:50]:
            print(f"  paths:+{lineno}: {key}", file=sys.stderr)
        if len(bad) > 50:
            print(f"  ... and {len(bad) - 50} more", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())