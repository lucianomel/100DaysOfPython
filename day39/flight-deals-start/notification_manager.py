from datetime import datetime
import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.msg = None
        self.sheet = {}
        self.price = None
        self.send_msg = False
        self.city = None

    def parse_data(self, data):
        price = data["price"]
        departure_city_name = data["cityFrom"]
        departure_airport_iata = data['cityCodeFrom']
        arrival_city_name = data['cityTo']
        arrival_airport_iata = data["cityCodeTo"]
        outbound_date = datetime.fromtimestamp(data["dTime"]).strftime("%Y-%m-%d")
        inbound_date = datetime.fromtimestamp(data["route"][1]['dTime']).strftime("%Y-%m-%d")

        msg = f"Low price alert! Only ${price} to fly from {departure_city_name}-{departure_airport_iata} to " \
              f"{arrival_city_name}-{arrival_airport_iata}, from {outbound_date} to {inbound_date}"

        self.city = arrival_city_name
        self.price = int(price)
        self.msg = msg

    def send_sms(self):
        if self.send_msg:
            account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
            auth_token = os.environ.get("TWILIO_AUTH_TOKEN")

            client = Client(account_sid, auth_token)

            message = client.messages.create(
                from_=os.environ.get("FROM_PHONE"),
                to=os.environ.get("TO_PHONE"),
                body=self.msg
            )
            print(message.sid)
            self.send_msg = False  # Stop sending messages

    def get_low_prices_sheet(self, sheet):
        self.sheet = sheet

    def compare_price(self):
        for flight_sheet in self.sheet['flights']:
            if flight_sheet['city'] == self.city and self.price < flight_sheet['lowestPrice']:
                print(f"send message {flight_sheet['city']} {self.price}<{flight_sheet['lowestPrice']}")
                self.send_msg = True
