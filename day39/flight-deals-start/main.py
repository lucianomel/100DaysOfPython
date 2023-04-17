from data_manager import DataManager
from flight_search import FlightSearch
from initial_data import iata_codes, flights_initial
from notification_manager import NotificationManager
from pprint import pprint

#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.


dm = DataManager()
fs = FlightSearch()
nm = NotificationManager()

# Get IATA codes
# sheet_data = dm.parse_initial_data()
#
# for index, data in enumerate(sheet_data):
#
#     iata_code = fs.get_iata_code(data["city"])
#     sheet_data[index]["iataCode"] = iata_code
# for row in sheet_data:
#     dm.update_iata_code(row)

# Send SMS for each low price
cities = []
for flight in flights_initial['flights']:
    cities.append(flight['city'])

low_prices_sheet = dm.get_low_prices_sheet()  # Sheety request
nm.get_low_prices_sheet(low_prices_sheet)
for city in cities:
    fs.get_city(city)
    data = fs.search_flights()
    nm.parse_data(data)
    nm.compare_price()
    nm.send_sms()

