from pathlib import Path
import json
from src.services.stock_crawler import StockCrawler
from src.services.data_sender import DataSender
import asyncio


async def main():
    stock_codes_path = Path("config/stock_codes.json")
    with stock_codes_path.open("r") as f:
        stock_codes = json.load(f)

    stock_codes = stock_codes["domestic"]

    crawler = StockCrawler(stock_codes)

    stocks = await crawler.crawl_stock_info()

    data_sender = DataSender(stocks)
    try:
        data_sender.send_data()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    asyncio.run(main())
