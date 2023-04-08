import requests
from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("OWM_API_KEY")
TO_PHONE = os.environ.get("TO_PHONE")

MY_LAT = "-34.615940"
MY_LONG = "-58.433449"

OWM_ENDPOINT = "https://api.openweathermap.org/data/2.8/onecall"
FROM_PHONE = os.environ.get("FROM_PHONE")


def api_call():
    parameters = {
        "lat": MY_LAT,
        "lon": MY_LONG,
        "appid": api_key,
        "exclude": "current,minutely,daily"
    }

    response = requests.get(OWM_ENDPOINT, params=parameters)

    response.raise_for_status()

    data = response.json()["hourly"]

    return data


def it_rains():
    data = api_call()
    first_twelve_hours = [item for index, item in enumerate(data) if index <= 12]  # Another way: slice v[:12]

    rains = False
    for weather_in_hour in first_twelve_hours:
        weather_id = weather_in_hour["weather"][0]["id"]
        if weather_id < 700:
            rains = True

    return rains


def send_sms():
    account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
    auth_token = os.environ.get("TWILIO_AUTH_TOKEN")

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_=FROM_PHONE,
        to=TO_PHONE,
        body="It's going to rain today! ☔ Remember to get an umbrella ☔"
    )
    print(message.sid)


def main():
    if it_rains():
        send_sms()


main()
