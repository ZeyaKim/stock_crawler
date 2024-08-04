import asyncio
from playwright.async_api import async_playwright, TimeoutError
from src.models.stock import Stock

NAVER_STOCK_BASE_URL = "https://m.stock.naver.com/domestic/stock/"


class StockCrawler:
    def __init__(self, stock_codes: list):
        self.stock_codes = stock_codes

    def create_stock_url(self, stock_code: str) -> str:
        return f"{NAVER_STOCK_BASE_URL}{stock_code}/total"

    async def crawl_stock_page(self, page, stock_code: str) -> dict:
        stock_url = self.create_stock_url(stock_code)
        await page.goto(stock_url)
        await page.wait_for_load_state("networkidle")

        stock_info = await self.crawl_by_xpath(page)

        return stock_info

        # return Stock(**stock_info)

    async def crawl_stock_info(self):
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()

            stock_infos = []
            for stock_code in self.stock_codes:
                info = await self.crawl_stock_page(page, stock_code)
                if info:
                    stock_infos.append(info)

            await browser.close()
            return stock_infos

    async def crawl_by_xpath(self, page):
        xpaths = {
            "stock_name": '//*[@id="content"]/div[2]/div[1]/div/span[2]',
            "price": '//*[@id="content"]/div[4]/div[3]/div/div[1]/ul/li[1]/div/span',
            "previous_day": '//*[@id="content"]/div[4]/div[3]/div/div[1]/ul/li[2]/div/span',
            "opening_price": '//*[@id="content"]/div[4]/div[3]/div/div[1]/ul/li[2]/div/span',
            "high_price": '//*[@id="content"]/div[4]/div[3]/div/div[1]/ul/li[3]/div/span',
            "low_price": '//*[@id="content"]/div[4]/div[3]/div/div[1]/ul/li[4]/div/span',
            "market_cap": '//*[@id="content"]/div[4]/div[3]/div/div[1]/ul/li[5]/div/span',
            "trading_volume": '//*[@id="content"]/div[4]/div[3]/div/div[1]/ul/li[6]/div/span',
            "trading_value": '//*[@id="content"]/div[4]/div[3]/div/div[1]/ul/li[7]/div/span',
            "foreign_ownership_ratio": '//*[@id="content"]/div[4]/div[3]/div/div[1]/ul/li[8]/div/span',
            "fifty_two_week_high": '//*[@id="content"]/div[4]/div[3]/div/div[1]/ul/li[9]/div/span',
            "fifty_two_week_low": '//*[@id="content"]/div[4]/div[3]/div/div[1]/ul/li[10]/div/span',
            "per": '//*[@id="content"]/div[4]/div[3]/div/div[1]/ul/li[11]/div/span',
            "eps": '//*[@id="content"]/div[4]/div[3]/div/div[1]/ul/li[12]/div/span',
            "forward_per": '//*[@id="content"]/div[4]/div[3]/div/div[1]/ul/li[13]/div/span',
            "forward_eps": '//*[@id="content"]/div[4]/div[3]/div/div[1]/ul/li[14]/div/span',
            "pbr": '//*[@id="content"]/div[4]/div[3]/div/div[1]/ul/li[15]/div/span',
            "bps": '//*[@id="content"]/div[4]/div[3]/div/div[1]/ul/li[16]/div/span',
            "dividend_yield": '//*[@id="content"]/div[4]/div[3]/div/div[1]/ul/li[17]/div/span',
            "expected_dividend_yield": '//*[@id="content"]/div[4]/div[3]/div/div[1]/ul/li[18]/div/span',
        }

        await page.click('//*[@id="content"]/div[4]/div[3]/div/div[1]/a')

        stock_info = {}

        for key, xpath in xpaths.items():
            try:
                stock_info[key] = await page.inner_text(xpath)
            except TimeoutError:
                stock_info[key] = None

        stock = Stock(**stock_info)

        return stock
