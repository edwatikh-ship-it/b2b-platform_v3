import requests
from bs4 import BeautifulSoup
async def scrape_yandex(query, depth):
    try:
        url = f"https://yandex.ru/search/?text={query.replace(' ', '+')}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36'
        }
        resp = requests.get(url, headers=headers, timeout=30)
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        urls = []
        for link in soup.find_all('a', href=True)[:depth*2]:
            href = link['href']
            if ('yandex.ru' in href or 'market.yandex.ru' in href) and href.startswith('http'):
                urls.append(href)
                if len(urls) >= depth:
                    break
        return urls if urls else [url]
    except Exception as e:
        return [f"Error: {str(e)}"]
