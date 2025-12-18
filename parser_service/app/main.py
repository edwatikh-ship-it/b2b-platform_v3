from __future__ import annotations

import os
import socket
import subprocess
import time
from typing import Any
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.yandex_playwright_scrape import scrape


app = FastAPI(title="Parser Service", version="0.2.0")


class ParseRequest(BaseModel):
    query: str
    depth: int = 1


def _chrome_exe_path() -> str:
    return os.getenv(
        "CHROME_EXE", r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    )


def _chrome_user_data_dir() -> str:
    return os.getenv(
        "CHROME_USER_DATA_DIR",
        os.path.join(os.environ["LOCALAPPDATA"], r"Google\Chrome\User Data"),
    )


def _chrome_profile_dir() -> str:
    return os.getenv("CHROME_PROFILE_DIR", "Default")


def _cdp_base_url() -> str:
    return os.getenv("CDP_URL", "http://127.0.0.1:9222")


def _cdp_version_url() -> str:
    return _cdp_base_url().rstrip("/") + "/json/version"


def _is_port_open(host: str, port: int, timeout_sec: float = 0.2) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout_sec):
            return True
    except OSError:
        return False


def ensure_cdp(timeout_sec: int = 10) -> dict[str, Any]:
    # Port-only gate: Python HTTP access to /json/version can return 503 even when CDP is usable.
    if _is_port_open("127.0.0.1", 9222):
        return {"cdp": "port-open"}

    chrome_exe = _chrome_exe_path()
    user_data = _chrome_user_data_dir()
    profile = _chrome_profile_dir()

    args = [
        chrome_exe,
        "--remote-debugging-port=9222",
        f"--user-data-dir={user_data}",
        f"--profile-directory={profile}",
    ]

    subprocess.Popen(
        args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, close_fds=True
    )  # noqa: S603

    deadline = time.time() + timeout_sec
    while time.time() < deadline:
        if _is_port_open("127.0.0.1", 9222):
            return {"cdp": "port-open"}
        time.sleep(0.25)

    raise RuntimeError(
        f"CDP did not start within {timeout_sec}s (port 9222 not reachable)."
    )


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/parse")
async def parse(payload: ParseRequest)
    # Guard: when client sends non-UTF-8 bytes, Cyrillic may arrive as "?????"
    if "?" in payload.query:
        raise HTTPException(
            status_code=400,
            detail="Query contains '?'. Likely encoding issue. Send Content-Type: application/json; charset=utf-8",
        ) -> dict[str, Any]:
    try:
        _ = ensure_cdp(timeout_sec=15)
    except RuntimeError as e:
        # Do not crash uvicorn; return a controlled 503 to the caller.
        raise HTTPException(status_code=503, detail=str(e)) from e

    urls = await scrape(
        query=payload.query, depth=payload.depth, cdp_url=_cdp_base_url()
    )
    return {"urls": urls}
