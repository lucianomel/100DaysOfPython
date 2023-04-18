import os
from dotenv import load_dotenv
from twilio.rest import Client
import smtplib

load_dotenv()


def parse_stop_overs(itineraries, departure_city, arrival_city):
    # Get every city that the plane goes through in stop-overs
    all_stop_over_cities = []
    for stop_over in itineraries:
        all_stop_over_cities.append(stop_over['cityTo'])
        all_stop_over_cities.append(stop_over['cityFrom'])

    # Get every city that's not dest or origin
    stop_overs_cities_w_reps = []
    for stop_over in all_stop_over_cities:
        if stop_over == departure_city or stop_over == arrival_city:
            continue
        else:
            stop_overs_cities_w_reps.append(stop_over)

    # Remove repeated cities
    stop_over_cities = list(dict.fromkeys(stop_overs_cities_w_reps))

    return stop_over_cities


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.msg = None
        self.sheet = {}
        self.price = None
        self.send_msg = False
        self.city = None
        self.user_emails = None

    def parse_data(self, data):
        global dest_index
        price = data["price"]
        departure_city_name = data["cityFrom"]
        departure_airport_iata = data["route"][0]['flyFrom']
        arrival_city_name = data['cityTo']

        destination_city_code_to = data['cityCodeTo']  # DPS
        origin_city_code_from = data['cityCodeFrom']  # LON

        stop_overs_itineraries = []
        for index, itinerary in enumerate(data['route']):
            if itinerary['cityCodeTo'] == destination_city_code_to:
                dest_index = index
            if itinerary['cityCodeTo'] != origin_city_code_from and \
                    itinerary['cityCodeFrom'] != origin_city_code_from:
                stop_overs_itineraries.append(itinerary)

        arrival_airport_iata = data["route"][dest_index]['flyTo']
        outbound_date = data["route"][0]['local_departure'].split("T")[0]
        inbound_date = data["route"][len(data['route'])-1]['local_arrival'].split("T")[0]

        msg = f"Low price alert! Only GBP${price} to fly from {departure_city_name}-{departure_airport_iata} to " \
              f"{arrival_city_name}-{arrival_airport_iata}, from {outbound_date} to {inbound_date}\n"

        if stop_overs_itineraries:
            msg += f"{len(data['route'])-2} stepovers, in"
            stop_over_cities = parse_stop_overs(stop_overs_itineraries, departure_city_name, arrival_city_name)
            for stop_over in stop_over_cities:
                msg += f" {stop_over}"
            msg += "."

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
        for flight_sheet_row in self.sheet['flights']:
            if flight_sheet_row['city'] == self.city and self.price < flight_sheet_row['lowestPrice']:
                print(f"send message {flight_sheet_row['city']} {self.price}<{flight_sheet_row['lowestPrice']}")
                self.send_msg = True

    def send_mails(self):
        """To  work need to call get_mails first"""
        if not self.user_emails:
            return
        if self.send_msg:
            my_email = os.environ["MY_MAIL"]
            my_password = os.environ["MAIL_PASSWORD"]
            for user_row in self.user_emails:
                with smtplib.SMTP("smtp.gmail.com") as connection:
                    connection.starttls()  # Encrypt email (tunnel)
                    connection.login(user=my_email, password=my_password)
                    connection.sendmail(
                        from_addr=my_email,
                        to_addrs=user_row["email"],
                        msg=f"Subject: Cheap Flight\n\nHello {user_row['firstName']} {user_row['lastName']}\n{self.msg}")
            self.send_msg = False

    def get_mails(self, mails):
        self.user_emails = mails
