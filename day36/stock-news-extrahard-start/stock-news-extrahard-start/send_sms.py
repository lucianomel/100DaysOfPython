import os
from dotenv import load_dotenv
from twilio.rest import Client
from stocks import get_delta_percentage
from news import get_articles,get_news_if_variation

load_dotenv()


## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number.
def send_sms(msg_body):
    account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
    auth_token = os.environ.get("TWILIO_AUTH_TOKEN")

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_=os.environ.get("FROM_PHONE"),
        to=os.environ.get("TO_PHONE"),
        body=msg_body
    )
    print(message.sid)


#Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""


def create_sms(articles, delta):
    msg = "TSLA: "
    if delta > 0:
        msg += "🔺"
    else:
        msg += "🔻"
    msg += str(abs(delta)) + "%\n"
    messages = [msg, msg, msg]
    i = 0
    for article in articles:
        messages[i] += "Headline: " + article["title"] + "\n"
        messages[i] += "Brief: " + article["description"] + "\n"
        i += 1
    return messages


def send_sms_tesla():
    delta_percentage = round(get_delta_percentage(), 3)
    articles = get_news_if_variation()
    if not articles:
        print(f"No significant variation, only {delta_percentage}%.")
        return
    else:
        messages = create_sms(articles, delta_percentage)
        for msg in messages:
            send_sms(msg_body=msg)
