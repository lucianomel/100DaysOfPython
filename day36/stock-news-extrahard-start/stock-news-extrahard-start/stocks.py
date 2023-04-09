import datetime as dt
from stock_data import stock_data
from main import THRESHOLD

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCKS_BASE_URL = "https://www.alphavantage.co/query"
NEWS_BASE_URL = "https://newsapi.org/v2/everything"

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").


def parse_stock_dates():
    last_day = dt.datetime.fromisoformat(max(stock_data))
    last_day_str = max(stock_data).split(" ")[0]
    previous_last_day_str = str(last_day+dt.timedelta(days=-1)).split(" ")[0]

    return {"yesterday": last_day_str, "day before": previous_last_day_str}


def get_delta_percentage():
    date_strings = parse_stock_dates()
    stock_price_yesterday = float(stock_data[date_strings["yesterday"]]['4. close'])
    stock_price_day_before = float(stock_data[date_strings["day before"]]['4. close'])
    delta_percentage = 100 - stock_price_yesterday*100/stock_price_day_before
    return delta_percentage


def are_news_needed():
    return get_delta_percentage() >= THRESHOLD
