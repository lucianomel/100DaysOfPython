import os
import requests
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

CAT_API_BASE_URL = "https://api.thecatapi.com/v1/images/search"
TO_PHONE = os.environ.get("TO_PHONE")
FROM_PHONE = os.environ.get("FROM_PHONE")


def send_cat_pic(cat_pic_url):
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
             media_url=[cat_pic_url],
             from_=f'whatsapp:{FROM_PHONE}',
             to=f'whatsapp:{TO_PHONE}',
             body="Hello human!"
         )

    print(message.sid)


def get_cat_pic_url():
    response = requests.get(CAT_API_BASE_URL)

    data = response.json()

    return data[0]["url"]


send_cat_pic(get_cat_pic_url())
