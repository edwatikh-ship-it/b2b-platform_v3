from fastapi import FastAPI
from pydantic import BaseModel
import logging
from yandex_playwright_scrape import scrape_yandex

app = FastAPI()
logging.basicConfig(level=logging.INFO)
log = logging.getLogger('main')

class ParseRequest(BaseModel):
    query: str
    depth: int = 5

@app.get('/health')
async def health():
    log.info('Health OK')
    return {'status': 'ok'}

@app.post('/parse')
async def parse(request: ParseRequest):
    log.info(f'Parse started: {request.query}')
    log.info(f'Calling scrape_yandex...')
    try:
        r = await scrape_yandex(request.query, request.depth)
        log.info(f'Parse success: {len(r)} results')
        return {'status': 'success', 'results': r}
    except Exception as e:
        log.error(f'Parse failed: {e}')
        return {'status': 'error', 'detail': str(e)}
