import json

from data_manager import DataManager
from flight_search import FlightSearch
from initial_data import iata_codes, flights_initial
from notification_manager import NotificationManager
from pprint import pprint

#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.


dm = DataManager()
fs = FlightSearch()
nm = NotificationManager()

# Update IATA codes
# low_prices_sheet = dm.get_low_prices_sheet() # Sheety request
#
# for index, data in enumerate(low_prices_sheet):
#     fs.get_city(data['city'])
#     iata_code = fs.get_iata_code()
#     low_prices_sheet[index]["iataCode"] = iata_code
# for row in low_prices_sheet:
#     dm.update_iata_code(row)

# Send SMS for each low price
try:
    with open("data.json", "r") as f:
        low_prices_sheet = json.load(f)
except FileNotFoundError:
    low_prices_sheet = dm.get_low_prices_sheet()  # Sheety request
    json_object = json.dumps(low_prices_sheet, indent=4)
    with open("data.json", "w") as f:
        f.write(json_object)

# Get user mails
nm.get_mails(dm.get_users_emails())


cities = [row['city'] for row in low_prices_sheet['flights']]

nm.get_low_prices_sheet(low_prices_sheet)
for city in cities:
    fs.get_city(city)
    data = fs.search_flights()
    if data:
        nm.compare_price()
        nm.parse_data(data)
        # nm.send_sms()
        nm.send_mails()

