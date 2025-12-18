from __future__ import annotations

from pathlib import Path
import argparse
import datetime as dt
import re

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE_ROOT = ROOT / "_log_archive"

# ВАЖНО:
# Удаляем только "болванки" вида <symptom>/<root_cause> и т.п.
# НЕЛЬЗЯ удалять строки по подстроке "INCIDENT", иначе можно снести реальные записи.
PLACEHOLDER_SNIPS = [
    "INCIDENT <symptom>",
    "<symptom>",
    "<root_cause>",
    "<fix>",
    "<fix_or_mitigation>",
    "<expected>",
]

def read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")

def write_text(p: Path, s: str) -> None:
    p.write_text(s.replace("\r\n", "\n").replace("\r", "\n"), encoding="utf-8", newline="\n")

def norm(s: str) -> str:
    s = s.strip()
    s = re.sub(r"\s+", " ", s)
    return s.lower()

def is_placeholder(line: str) -> bool:
    l = line.lower()
    return any(x.lower() in l for x in PLACEHOLDER_SNIPS)

def dedupe(lines: list[str]) -> list[str]:
    seen = set()
    out: list[str] = []
    for ln in lines:
        if is_placeholder(ln):
            continue
        key = norm(ln)
        if key and key in seen:
            continue
        if key:
            seen.add(key)
        out.append(ln.rstrip())
    return out

def make_handoff(src: str) -> str:
    lines = dedupe(src.splitlines())
    header = [
        "# HANDOFF  B2B Platform",
        "",
        "Канонический лог успехов (сгенерён tools/regen_logs.py).",
        "Оригиналы сохраняются в _log_archive/ (timestamped).",
        "",
        "## Правило (DoD)",
        "- Успех  сюда: datetime MSK, what changed, verify cmd  expected.",
        "- Фейл  INCIDENTS.md (symptom/root cause/fix/verify).",
        "",
        "## Entries (append-only, logically)",
        "",
    ]
    return "\n".join(header) + "\n".join(lines).strip() + "\n"

def make_incidents(src: str) -> str:
    lines = dedupe(src.splitlines())
    header = [
        "# INCIDENTS  B2B Platform",
        "",
        "Канонический список инцидентов/граблей (сгенерён tools/regen_logs.py).",
        "Оригиналы сохраняются в _log_archive/ (timestamped).",
        "",
        "## Правило",
        "- Append-only по смыслу (история сохраняется через архивирование).",
        "- Формат: datetime MSK  symptom  root cause  fix/mitigation  verification (cmd  expected).",
        "- Без длинных логов/трейсбеков.",
        "",
        "## Entries (append-only, logically)",
        "",
    ]
    out = "\n".join(header) + "\n".join(lines).strip() + "\n"

    # Safety check: чтобы не съесть файл
    msk_lines = sum(1 for ln in out.splitlines() if " MSK" in ln)
    if msk_lines < 20:
        raise SystemExit(f"FATAL: too few MSK lines in INCIDENTS.md after regen: {msk_lines}")

    # Дополнительная защита: должен остаться хотя бы один INCIDENT
    if "incident" not in out.lower():
        raise SystemExit("FATAL: no 'INCIDENT' word found after regen (suspicious)")

    return out

def main() -> int:
    ap = argparse.ArgumentParser(description="Regenerate HANDOFF.md and INCIDENTS.md from current logs, archiving originals.")
    ap.add_argument("--dry-run", action="store_true", help="Do not write changes, only print what would happen.")
    args = ap.parse_args()

    handoff = ROOT / "HANDOFF.md"
    incidents = ROOT / "INCIDENTS.md"

    if not handoff.exists() or not incidents.exists():
        raise SystemExit("FATAL: HANDOFF.md or INCIDENTS.md not found in repo root")

    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    archive_dir = ARCHIVE_ROOT / stamp

    new_handoff = make_handoff(read_text(handoff))
    new_incidents = make_incidents(read_text(incidents))

    if args.dry_run:
        print(f"DRY RUN: would archive to {archive_dir}")
        print("DRY RUN: would rewrite HANDOFF.md and INCIDENTS.md")
        return 0

    archive_dir.mkdir(parents=True, exist_ok=True)

    # archive originals
    write_text(archive_dir / "HANDOFF.md", read_text(handoff))
    write_text(archive_dir / "INCIDENTS.md", read_text(incidents))

    # rewrite canonical logs
    write_text(handoff, new_handoff)
    write_text(incidents, new_incidents)

    print(f"OK: archived originals to {archive_dir}")
    print("OK: rewrote HANDOFF.md and INCIDENTS.md")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())