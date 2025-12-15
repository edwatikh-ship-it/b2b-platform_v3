import os
import subprocess
import time
from typing import Any

import httpx
from fastapi import FastAPI
from pydantic import BaseModel

from app.yandex_playwright_scrape import scrape


app = FastAPI(title="Parser Service", version="0.2.0")


class ParseRequest(BaseModel):
    query: str
    depth: int = 1


def _chrome_exe_path() -> str:
    return os.getenv("CHROME_EXE", r"C:\Program Files\Google\Chrome\Application\chrome.exe")


def _chrome_user_data_dir() -> str:
    return os.getenv("CHROME_USER_DATA_DIR", os.path.join(os.environ["LOCALAPPDATA"], r"Google\Chrome\User Data"))


def _chrome_profile_dir() -> str:
    return os.getenv("CHROME_PROFILE_DIR", "Default")


def _cdp_base_url() -> str:
    return os.getenv("CDP_URL", "http://127.0.0.1:9222")


def _cdp_version_url() -> str:
    return _cdp_base_url().rstrip("/") + "/json/version"


def ensure_cdp(timeout_sec: int = 10) -> dict[str, Any]:
    try:
        r = httpx.get(_cdp_version_url(), timeout=1.5)
        r.raise_for_status()
        return r.json()
    except Exception:
        pass

    chrome_exe = _chrome_exe_path()
    user_data = _chrome_user_data_dir()
    profile = _chrome_profile_dir()

    args = [
        chrome_exe,
        "--remote-debugging-port=9222",
        f"--user-data-dir={user_data}",
        f"--profile-directory={profile}",
    ]

    subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, close_fds=True)  # noqa: S603

    deadline = time.time() + timeout_sec
    last_err: str | None = None
    while time.time() < deadline:
        try:
            r = httpx.get(_cdp_version_url(), timeout=1.5)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            last_err = str(e)
            time.sleep(0.25)

    raise RuntimeError(f"CDP did not start within {timeout_sec}s. Last error: {last_err}")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/parse")
async def parse(payload: ParseRequest) -> dict[str, Any]:
    # гарантируем, что Chrome CDP поднят
    _ = ensure_cdp(timeout_sec=15)

    urls = await scrape(query=payload.query, depth=payload.depth, cdp_url=_cdp_base_url())
    return {"urls": urls}
