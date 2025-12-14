set shell := ["powershell.exe", "-NoProfile", "-Command"]

lint:
  cd backend; .\.venv\Scripts\python.exe -m ruff check .

fmt:
  cd backend; .\.venv\Scripts\python.exe -m ruff check . --fix
  cd backend; .\.venv\Scripts\python.exe -m ruff format .

test:
  cd backend; $env:PYTHONPATH="D:\b2bplatform\backend"; .\.venv\Scripts\python.exe -m pytest -q

clean:
  Remove-Item -Recurse -Force -ErrorAction SilentlyContinue backend\.pytest_cache, backend\__pycache__, backend\app\__pycache__