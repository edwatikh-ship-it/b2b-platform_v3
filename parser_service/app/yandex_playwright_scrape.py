import asyncio
import random
import logging
import urllib.parse
import time

from playwright.async_api import async_playwright

logging.basicConfig(
    filename="parser.log",
    filemode="a",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Сколько максимум “терпим” модалки/попапы/подвисания на одном движке
ENGINE_BUDGET_SEC = 300  # 5 минут


# ------------------- HELPERS -------------------
async def human_pause(a: float = 1.5, b: float = 4.5) -> None:
    await asyncio.sleep(random.uniform(a, b))


async def human_scroll(page) -> None:
    actions = [
        lambda: page.mouse.wheel(0, random.randint(200, 600)),
        lambda: page.mouse.wheel(0, random.randint(-300, -100)),
        lambda: page.mouse.wheel(0, random.randint(50, 150)),
    ]
    for _ in range(random.randint(1, 3)):
        await actions[random.randint(0, len(actions) - 1)]()
        await human_pause(0.4, 1.2)


async def human_mouse_movement(page) -> None:
    x = random.randint(100, 900)
    y = random.randint(100, 700)
    for _ in range(random.randint(2, 6)):
        xr = x + random.randint(-30, 30)
        yr = y + random.randint(-30, 30)
        await page.mouse.move(xr, yr, steps=random.randint(6, 22))
        await human_pause(0.2, 0.6)


async def very_human_behavior(page) -> None:
    await human_pause()
    await human_mouse_movement(page)
    await human_pause(0.5, 2)
    await human_scroll(page)
    await human_pause(1, 3)


async def bring_to_front_safe(page) -> None:
    try:
        await page.bring_to_front()
    except Exception:
        pass


async def dismiss_popups_best_effort(page) -> None:
    # “по умолчанию”, “выбрать город”, “принять”, “закрыть” и т.п.
    candidates = [
        "button:has-text('Использовать по умолчанию')",
        "button:has-text('Сделать по умолчанию')",
        "button:has-text('Выбрать город')",
        "button:has-text('Выбрать')",
        "button:has-text('Ок')",
        "button:has-text('OK')",
        "button:has-text('Понятно')",
        "button:has-text('Не сейчас')",
        "button:has-text('Позже')",
        "button:has-text('Нет, спасибо')",
        "button:has-text('Отмена')",
        "button:has-text('Закрыть')",
        "[aria-label='Закрыть']",
        "[aria-label='Close']",
        ".modal__close",
        ".popup__close",
        "button[title='Закрыть']",
    ]

    for _ in range(4):
        try:
            for sel in candidates:
                loc = page.locator(sel)
                if await loc.count() > 0:
                    try:
                        await loc.first.click(timeout=800)
                        await human_pause(0.2, 0.6)
                    except Exception:
                        pass
        except Exception:
            pass


async def wait_for_captcha(page, engine_name: str) -> None:
    while True:
        url = page.url.lower()
        if "captcha" in url or "showcaptcha" in url:
            logging.warning("%s: captcha detected, waiting for manual solve", engine_name)
            await bring_to_front_safe(page)
            print(f"{engine_name}: solve captcha in the browser, waiting...")
            await asyncio.sleep(2)
        else:
            break


# ------------------- PARSERS -------------------
async def parse_yandex(page, query: str, pages: int, collected_links: set[str]) -> None:
    deadline = time.time() + ENGINE_BUDGET_SEC

    query2 = f"{query} купить"
    encoded = urllib.parse.quote_plus(query2)

    await bring_to_front_safe(page)
    await page.goto(
        f"https://yandex.ru/search/?text={encoded}",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    await dismiss_popups_best_effort(page)
    await wait_for_captcha(page, "YANDEX")

    for n in range(1, pages + 1):
        if time.time() > deadline:
            logging.warning("YANDEX: budget exceeded, stopping")
            return

        logging.info("YANDEX: parsing page %s", n)

        await very_human_behavior(page)
        await dismiss_popups_best_effort(page)
        await wait_for_captcha(page, "YANDEX")

        elems = page.locator("a.Link")
        count = await elems.count()
        for i in range(count):
            href = await elems.nth(i).get_attribute("href")
            if href and href.startswith("http") and ".ru" in href:
                collected_links.add(href.split("?")[0])

        next_btn = page.locator("a[aria-label='Следующая страница']")
        if await next_btn.count() == 0:
            break

        await human_pause(3, 10)
        await dismiss_popups_best_effort(page)
        await next_btn.click()
        await wait_for_captcha(page, "YANDEX")


async def parse_google(page, query: str, pages: int, collected_links: set[str]) -> None:
    deadline = time.time() + ENGINE_BUDGET_SEC

    query2 = f"{query} купить"
    encoded = urllib.parse.quote_plus(query2)

    await bring_to_front_safe(page)
    # Google часто “не доходит” до события load — поэтому domcontentloaded + длинный timeout
    await page.goto(
        f"https://www.google.com/search?q={encoded}&hl=ru",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    await dismiss_popups_best_effort(page)
    await wait_for_captcha(page, "GOOGLE")

    for n in range(1, pages + 1):
        if time.time() > deadline:
            logging.warning("GOOGLE: budget exceeded, stopping")
            return

        logging.info("GOOGLE: parsing page %s", n)

        await very_human_behavior(page)
        await dismiss_popups_best_effort(page)
        await wait_for_captcha(page, "GOOGLE")

        elems = page.locator("a")
        count = await elems.count()
        for i in range(count):
            href = await elems.nth(i).get_attribute("href")
            if href and href.startswith("http") and ".ru" in href and "google" not in href:
                collected_links.add(href.split("&")[0])

        next_btn = page.locator("a#pnnext")
        if await next_btn.count() == 0:
            break

        await human_pause(3, 10)
        await dismiss_popups_best_effort(page)
        await next_btn.click()
        await wait_for_captcha(page, "GOOGLE")


# ------------------- PUBLIC API -------------------
async def scrape(query: str, depth: int, cdp_url: str = "http://127.0.0.1:9222") -> list[str]:
    collected_links: set[str] = set()

    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(cdp_url)
        context = browser.contexts[0] if browser.contexts else await browser.new_context()

        y_page = await context.new_page()
        g_page = await context.new_page()

        results = await asyncio.gather(
            parse_yandex(y_page, query, depth, collected_links),
            parse_google(g_page, query, depth, collected_links),
            return_exceptions=True,
        )

        for r in results:
            if isinstance(r, Exception):
                logging.exception("one of parsers failed", exc_info=r)

    return sorted(collected_links)


# ------------------- CLI (optional) -------------------
async def main() -> None:
    query = input("Введите поисковый запрос: ").strip()
    depth = int(input("Введите глубину поиска (кол-во страниц): "))
    urls = await scrape(query=query, depth=depth, cdp_url="http://127.0.0.1:9222")
    print(f"Найдено .RU ссылок: {len(urls)}")


if __name__ == "__main__":
    asyncio.run(main())