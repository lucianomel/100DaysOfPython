from stocks import parse_stock_dates
import os
import requests
from dotenv import load_dotenv
from util import save_api_call

COMPANY_NAME = "Tesla Inc"
NEWS_BASE_URL = "https://newsapi.org/v2/everything"


load_dotenv()


def api_call_news():
    dates = parse_stock_dates()
    print(dates)
    parameters = {
        "q": COMPANY_NAME,
        "from": dates["yesterday"],
        "to": dates["day before"],
        "language": "en",
        "pageSize": 3,
        "apiKey": os.environ.get("NEWS_API_KEY")
    }
    response = requests.get(NEWS_BASE_URL, params=parameters)
    response.raise_for_status()
    return response


news_data = save_api_call("news_data", api_caller=api_call_news)["articles"]
