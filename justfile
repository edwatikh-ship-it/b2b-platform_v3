# Chrome CDP (9222) for parser_service
chrome-cdp:
  powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\start_chrome_cdp.ps1
set shell := ["powershell.exe", "-NoProfile", "-Command"]

# Backend (reload)
dev:
  cd backend; $env:PYTHONPATH="D:\b2bplatform\backend"; .\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

# Backend stable
dev-noreload:
  cd backend; $env:PYTHONPATH="D:\b2bplatform\backend"; .\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000

# Parser service
parser: chrome-cdp
  cd parser_service; python -m uvicorn app.main:app --host 127.0.0.1 --port 9001

# Start both (two windows)
up:
  Start-Process powershell -ArgumentList "-NoProfile","-NoExit","-Command","Set-Location D:\b2bplatform; just dev-noreload"
  Start-Process powershell -ArgumentList "-NoProfile","-NoExit","-Command","Set-Location D:\b2bplatform; just parser"

# Smoke checks:
# - backend must return health + openapi.json
# - parser_service only needs to respond (404 is OK)
smoke:
  Invoke-RestMethod "http://127.0.0.1:8000/health" | Out-Null
  Invoke-RestMethod "http://127.0.0.1:8000/openapi.json" | Out-Null
  try { (Invoke-WebRequest "http://127.0.0.1:9001/" -UseBasicParsing -TimeoutSec 2).StatusCode | Out-Null } catch { if ($_.Exception.Response -and $_.Exception.Response.StatusCode) { [int]$_.Exception.Response.StatusCode | Out-Null } else { throw } }

lint:
  cd backend; .\.venv\Scripts\python.exe -m ruff check .

fmt:
  cd backend; .\.venv\Scripts\python.exe -m ruff check . --fix
  cd backend; .\.venv\Scripts\python.exe -m ruff format .

test:
  cd backend; $env:PYTHONPATH="D:\b2bplatform\backend"; .\.venv\Scripts\python.exe -m pytest -q

clean:
  Remove-Item -Recurse -Force -ErrorAction SilentlyContinue backend\.pytest_cache, backend\__pycache__, backend\app\__pycache__, parser_service\__pycache__, parser_service\app\__pycache__

# Update curated project tree (key artifacts)
tree:
    powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\update_project_tree.ps1
# Dump context for a new chat (read-only, paste output into chat)
chat-bundle:
  powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\new-chat-bundle.ps1
# Print the prompt to paste into a new chat
new-chat-prompt:
  @powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\new_chat_prompt.ps1
# Alias: canonical prompt generator
prompt:
  @just new-chat-prompt
# Alias: canonical prompt generator


# Aliases
backend:
    just dev

backend-noreload:
    just dev-noreload
# Print the prompt (v2) to paste into a new chat (does NOT change old prompt)
prompt2:
  @powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\new_chat_prompt2.ps1
/endpoint-status PATH:
    #!/usr/bin/env pwsh -NoProfile -ExecutionPolicy Bypass
    $path = "{{PATH}}"
    echo "Status: /$path"
    try {
        $r = Invoke-RestMethod "http://127.0.0.1:8000$path?limit=1" -ErrorAction Stop
        echo "  → 200 OK (implemented)"
    } catch {
        if ($_.Exception.Response.StatusCode -eq 501) {
            echo "  → 501 Not Implemented (stub OK)"
        } else {
            echo "  → {{$_.Exception.Response.StatusCode}} ERROR"
        }
    }

/stub-endpoint PATH:
    #!/usr/bin/env pwsh -NoProfile -ExecutionPolicy Bypass
    echo "TODO: create 501 stub + test for {{PATH}}"
