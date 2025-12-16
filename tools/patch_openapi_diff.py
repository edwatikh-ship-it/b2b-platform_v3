from __future__ import annotations

from pathlib import Path

PATH = Path("tools/openapi_diff.py")


def must_contain(s: str, needle: str) -> None:
    if needle not in s:
        raise SystemExit(f"STOP: anchor not found: {needle}")


def main() -> int:
    raw = PATH.read_text(encoding="utf-8")

    # anchors
    must_contain(raw, '"--live-url"')
    must_contain(raw, "if args.live_url:")
    must_contain(raw, "live = load_live_from_url(args.live_url, args.timeout)")
    must_contain(raw, "live_path = Path(args.live_file)")
    must_contain(raw, "return 0")

    # 1) insert new arg --openapi-url-env after the closing ')' of the --live-url add_argument
    lines = raw.splitlines(keepends=True)
    out = []
    in_live_url_add = False
    inserted = False

    for line in lines:
        out.append(line)
        if '"--live-url"' in line:
            in_live_url_add = True
            continue
        if in_live_url_add and line.strip() == ")":
            if not inserted:
                out.append(
                    "    p.add_argument(\n"
                    '        "--openapi-url-env",\n'
                    '        default="OPENAPI_URL",\n'
                    '        help="Env var name used when --live-url is not set (default: OPENAPI_URL).",\n'
                    "    )\n"
                )
                inserted = True
            in_live_url_add = False

    if not inserted:
        raise SystemExit(
            "STOP: failed to insert --openapi-url-env (could not detect end of --live-url add_argument)."
        )

    raw2 = "".join(out)

    # 2) replace load-live logic (exact block with \n)
    old_block = (
        "    if args.live_url:\n"
        "        live = load_live_from_url(args.live_url, args.timeout)\n"
        "    else:\n"
        "        live_path = Path(args.live_file)\n"
        "        if not live_path.exists():\n"
        "            raise SystemExit(\n"
        '                f"Live file not found: {live_path}. Provide --live-url or create the file."\n'
        "            )\n"
        "        live = load_live_from_file(live_path)\n"
    )

    new_block = (
        "    live_url = args.live_url\n"
        "    if not live_url:\n"
        "        import os\n"
        "        live_url = os.getenv(args.openapi_url_env)\n"
        "\n"
        "    if live_url:\n"
        "        live = load_live_from_url(live_url, args.timeout)\n"
        "    else:\n"
        "        live_path = Path(args.live_file)\n"
        "        if not live_path.exists():\n"
        "            raise SystemExit(\n"
        '                f"Live file not found: {live_path}. Provide --live-url or set {args.openapi_url_env}."\n'
        "            )\n"
        "        live = load_live_from_file(live_path)\n"
    )

    must_contain(raw2, old_block)
    raw3 = raw2.replace(old_block, new_block, 1)

    # 3) replace the mojibake print block in a simple way:
    # if there's any print(...) containing args.out/missing/extra/present, replace that whole statement.
    idx = raw3.find("print(")
    replaced_print = False
    while idx != -1:
        end = raw3.find(")\n", idx)
        if end == -1:
            break
        chunk = raw3[idx : end + 2]
        if (
            ("args.out" in chunk)
            and ("missing" in chunk)
            and ("extra" in chunk)
            and ("present" in chunk)
        ):
            raw3 = (
                raw3[:idx]
                + '    print(f"OK {args.out}: {len(missing)} missing, {len(extra)} extra, {len(present)} ok")\n'
                + raw3[end + 2 :]
            )
            replaced_print = True
            break
        idx = raw3.find("print(", end + 2)

    if not replaced_print:
        # don't fail hard here; print fix is nice-to-have, env fix is the main goal
        pass

    PATH.write_text(raw3, encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
