from __future__ import annotations

import argparse
import datetime as dt
import pathlib
import re
import sys

ROOT = pathlib.Path(r"D:\b2bplatform")
BACKUPS = ROOT / ".tmp" / "backups"


def utc_timestamp() -> str:
    # timestamp string, local time is OK for backup filenames
    return dt.datetime.now().strftime("%Y%m%d-%H%M%S")


def read_text(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8")


def write_utf8_nobom(path: pathlib.Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def backup_file(path: pathlib.Path, tag: str) -> pathlib.Path:
    BACKUPS.mkdir(parents=True, exist_ok=True)
    dst = BACKUPS / f"{path.name}.bak.{tag}.{utc_timestamp()}"
    dst.write_bytes(path.read_bytes())
    return dst


def normalize_lf(path_str: str) -> int:
    p = (ROOT / path_str).resolve() if not pathlib.Path(path_str).is_absolute() else pathlib.Path(path_str)
    if not p.exists():
        raise FileNotFoundError(f"File not found: {p}")
    backup_file(p, "doc-edit-py")
    txt = read_text(p).replace("\r\n", "\n")
    write_utf8_nobom(p, txt)
    return 0


def fix_incident_project_tree() -> int:
    p = (ROOT / "INCIDENTS.md").resolve()
    if not p.exists():
        raise FileNotFoundError("INCIDENTS.md not found in repo root")

    backup_file(p, "doc-edit-py")

    txt = read_text(p)

    anchor = "## 2025-12-18 00:52 MSK  Incident: Suggested missing just recipe (project-tree)"
    start = txt.find(anchor)
    if start < 0:
        raise RuntimeError(f"Anchor not found in INCIDENTS.md: {anchor}")

    next_idx = txt.find("\n## ", start + 1)
    if next_idx < 0:
        next_idx = len(txt)

    before = txt[:start]
    after = txt[next_idx:]

    replacement = (
        "## 2025-12-18 00:52 MSK  Incident: Suggested missing just recipe (project-tree)\n\n"
        "- Symptom:\n"
        "  - `just -n project-tree` and `just project-tree` failed with: \"Justfile does not contain recipe `project-tree`\".\n"
        "- Root cause:\n"
        "  - Assistant suggested a just recipe without verifying it exists first (`just -n {recipe}` or `just --list`).\n"
        "- Fix/Mitigation:\n"
        "  - Plan B: update PROJECT-TREE.txt via:\n"
        "    - powershell -NoProfile -ExecutionPolicy Bypass -File .\\tools\\update_project_tree.ps1\n"
        "  - Follow the process rule: Commands-first gate (HARD) + STOP until facts are pasted.\n"
        "- Verification:\n"
        "  - powershell -NoProfile -ExecutionPolicy Bypass -File .\\tools\\update_project_tree.ps1\n"
        "  - Expected: \"Wrote PROJECT-TREE.txt with {N} paths.\"\n\n"
    )

    out = (before + replacement + after).replace("\r\n", "\n")
    write_utf8_nobom(p, out)
    return 0


def agent_pattern_just_recipe() -> int:
    p = (ROOT / "AGENT-KNOWLEDGE.md").resolve()
    if not p.exists():
        raise FileNotFoundError("AGENT-KNOWLEDGE.md not found in repo root")

    txt = read_text(p)

    # Idempotent: if already present, do nothing.
    if "### Just recipe verification (commands-first)" in txt:
        return 0

    rx = re.compile(r"(?m)^(##\s+Incident patterns\s*)\r?\n-\s*TBD\s*(\r?\n)")
    if not rx.search(txt):
        raise RuntimeError("Insert point not found: expected '## Incident patterns' followed by '- TBD'")

    backup_file(p, "doc-edit-py")

    block = (
        r"\1\n"
        "### Just recipe verification (commands-first)\n\n"
        "Trigger:\n"
        "- Need to suggest running a `just {recipe}` command (or claim a recipe exists).\n\n"
        "Checks (facts first):\n"
        "- `just --list` (preferred) OR `just -n {recipe}`.\n"
        "- If the recipe is missing: do NOT suggest it; switch to Plan B (explicit commands/script path).\n\n"
        "Decision:\n"
        "- If recipe exists: suggest the exact `just {recipe}` command.\n"
        "- If recipe does not exist: suggest Plan B (e.g., `powershell -NoProfile -ExecutionPolicy Bypass -File .\\tools\\update_project_tree.ps1`).\n\n"
        "Verify:\n"
        "- Paste the output of `just --list` or `just -n {recipe}` before proceeding.\n"
        r"\2"
    )

    out = rx.sub(block, txt).replace("\r\n", "\n")
    write_utf8_nobom(p, out)
    return 0

def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    s1 = sub.add_parser("normalize-lf")
    s1.add_argument("--path", required=True)

    sub.add_parser("fix-incident-project-tree")
    sub.add_parser("agent-pattern-just-recipe")

    args = ap.parse_args(argv)

    if args.cmd == "normalize-lf":
        return normalize_lf(args.path)
    if args.cmd == "fix-incident-project-tree":
        return fix_incident_project_tree()
    if args.cmd == "agent-pattern-just-recipe":
        return agent_pattern_just_recipe()

    raise RuntimeError("Unknown command")


if __name__ == "__main__":
    try:
        raise SystemExit(main(sys.argv[1:]))
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        raise
