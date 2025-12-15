from __future__ import annotations

from pathlib import Path
import sys


API_PATH = Path(r"D:\b2bplatform\api-contracts.yaml")


def main() -> int:
    api_path = API_PATH
    if not api_path.exists():
        print(f"ERROR: not found: {api_path}", file=sys.stderr)
        return 2

    lines = api_path.read_text(encoding="utf-8").splitlines(keepends=True)

    changed = 0
    i = 0
    n = len(lines)

    while i < n:
        # We only target query parameters with exact name "limit"
        if lines[i].strip() == "- name: limit":
            # Confirm it is a query param (in: query) within the next few lines.
            window_end = min(i + 30, n)
            is_query = any(
                lines[j].strip() == "in: query" for j in range(i, window_end)
            )
            if not is_query:
                i += 1
                continue

            # Find schema -> type: integer
            type_idx = None
            for j in range(i, window_end):
                if lines[j].rstrip("\n") == "          type: integer":
                    type_idx = j
                    break

            if type_idx is None:
                i += 1
                continue

            # If maximum already present right after type, skip
            if (
                type_idx + 1 < n
                and lines[type_idx + 1].rstrip("\n") == "          maximum: 200"
            ):
                i += 1
                continue

            # Insert maximum right after type (same indent level)
            lines.insert(type_idx + 1, "          maximum: 200\n")
            changed += 1
            n += 1
            i = type_idx + 2
            continue

        i += 1

    if changed == 0:
        print("No changes needed: all query limit already have maximum: 200")
        return 0

    api_path.write_text("".join(lines), encoding="utf-8", newline="\n")
    print(f"Updated {changed} limit parameter(s) with maximum: 200")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
