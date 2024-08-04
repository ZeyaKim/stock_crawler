import datetime
import httpx
from src.models.stock import Stock
import os

SHEET_URL = os.getenv("POST_URL")


class DataSender:
    def __init__(self, stock_infos: list[Stock]):
        self.stock_infos = stock_infos

    def send_data(self):
        request_data = self.create_request_data(self.stock_infos)

        with httpx.Client() as client:
            response = client.post(
                SHEET_URL,
                json=request_data,
                headers={"Content-Type": "application/json"},
                follow_redirects=True,
            )

            if response.status_code != 200:
                raise Exception(
                    f"Failed to send data to Google Sheet : {response.status_code}"
                )
            else:
                print("Data sent successfully")

    def create_request_data(self, stock_infos: list[Stock]):
        now = datetime.datetime.now()

        return {
            "metadata": {
                "date": now.strftime("%Y-%m-%d"),
                "time": now.strftime("%H:%M:%S"),
                "count": len(stock_infos),
            },
            "stocks": [stock.to_dict() for stock in stock_infos],
        }
