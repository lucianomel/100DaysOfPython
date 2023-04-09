from news_data import news_data
from stocks import are_news_needed

# STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.


def get_news_if_variation():
    """If increase/decrease by 5% returns the news, if not returns None"""
    if are_news_needed():
        return news_data
    else:
        return None


def get_articles():
    """Used to test"""
    return news_data
