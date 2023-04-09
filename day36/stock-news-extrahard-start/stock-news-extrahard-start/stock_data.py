import os
import requests
from dotenv import load_dotenv
from util import save_api_call

STOCK = "TSLA"
STOCKS_BASE_URL = "https://www.alphavantage.co/query"

load_dotenv()


def api_call_stock_price():
    parameters = {
        "function": "TIME_SERIES_DAILY_ADJUSTED",
        "symbol": STOCK,
        "outputsize": "compact",
        "apikey": os.environ.get("ALPHA_API_KEY")
    }
    response = requests.get(STOCKS_BASE_URL, params=parameters)
    response.raise_for_status()

    return response


stock_data = save_api_call("stock_price", api_caller=api_call_stock_price)["Time Series (Daily)"]
