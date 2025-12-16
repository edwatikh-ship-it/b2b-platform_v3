import argparse
import json
from pathlib import Path

import requests
import yaml


def load_contract(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_live_from_file(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_live_from_url(url: str, timeout: int) -> dict:
    resp = requests.get(url, timeout=timeout)
    resp.raise_for_status()
    return resp.json()


def main() -> int:
    p = argparse.ArgumentParser(
        description="Diff SSoT api-contracts.yaml paths vs runtime OpenAPI."
    )
    p.add_argument(
        "--contract",
        default="api-contracts.yaml",
        help="Path to SSoT OpenAPI YAML (default: api-contracts.yaml).",
    )
    p.add_argument(
        "--live-file",
        default=".tmp/runtime-openapi.json",
        help="Path to runtime OpenAPI JSON snapshot (default: .tmp/runtime-openapi.json).",
    )
    p.add_argument(
        "--live-url",
        default=None,
        help="Runtime OpenAPI URL, e.g. http://127.0.0.1:8000/openapi.json. If set, uses HTTP.",
    )
    p.add_argument(
        "--openapi-url-env",
        default="OPENAPI_URL",
        help="Env var name used when --live-url is not set (default: OPENAPI_URL).",
    )
    p.add_argument(
        "--timeout", type=int, default=10, help="HTTP timeout seconds (default: 10)."
    )
    p.add_argument(
        "--out",
        default="openapi-diff.csv",
        help="Output CSV path (default: openapi-diff.csv).",
    )
    args = p.parse_args()

    contract = load_contract(Path(args.contract))

    live_url = args.live_url
    if not live_url:
        import os

        live_url = os.getenv(args.openapi_url_env)

    if live_url:
        live = load_live_from_url(live_url, args.timeout)
    else:
        live_path = Path(args.live_file)
        if not live_path.exists():
            raise SystemExit(
                f"Live file not found: {live_path}. Provide --live-url or set {args.openapi_url_env}."
            )
        live = load_live_from_file(live_path)

    contract_paths = set(contract.get("paths", {}).keys())
    live_paths = set(live.get("paths", {}).keys())

    missing = sorted(contract_paths - live_paths)
    extra = sorted(live_paths - contract_paths)
    present = sorted(contract_paths & live_paths)

    with open(args.out, "w", encoding="utf-8") as out:
        out.write("status,path,method,operationId\n")

        for path in missing:
            for method, spec in contract["paths"][path].items():
                if method in ["get", "post", "put", "delete", "patch"]:
                    op = (spec or {}).get("operationId", "")
                    out.write(f'MISSING,"{path}",{method.upper()},{op}\n')

        for path in extra:
            for method, spec in live["paths"][path].items():
                if method in ["get", "post", "put", "delete", "patch"]:
                    op = (spec or {}).get("operationId", "")
                    out.write(f'EXTRA,"{path}",{method.upper()},{op}\n')

        for path in present:
            for method, spec in contract["paths"][path].items():
                if method in ["get", "post", "put", "delete", "patch"]:
                    op = (spec or {}).get("operationId", "")
                    out.write(f'OK,"{path}",{method.upper()},{op}\n')

        print(
            f"OK {args.out}: {len(missing)} missing, {len(extra)} extra, {len(present)} ok"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
