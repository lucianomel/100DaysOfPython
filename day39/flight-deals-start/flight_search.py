import os
import requests
from datetime import datetime,timedelta
from pprint import pprint

TEKILA_BASE_URL = "https://api.tequila.kiwi.com"


class FlightSearch:
    # This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self.city = None
        self.iata_code = None

    def get_city(self, city):
        self.city = city

    def get_iata_code(self):
        auth_headers = {
            "apikey": os.environ["KIWI_API_KEY"]
        }
        request_config = {
            "term": self.city,
            "limit": 1,
            "location_types": "city"
        }
        response = requests.get(url=f"{TEKILA_BASE_URL}/locations/query", params=request_config, headers=auth_headers)
        response.raise_for_status()
        data = response.json()
        self.iata_code = data["locations"][0]["code"]
        return self.iata_code

    def search_flights(self):
        self.get_iata_code()
        auth_headers = {
            "apikey": os.environ["KIWI_API_KEY"]
        }
        day_in_six_months = (datetime.now()+timedelta(days=(6*30))).strftime("%d/%m/%Y")
        tomorrow = datetime.now().strftime("%d/%m/%Y")
        request_config = {
            "fly_from": "LON",
            "fly_to": self.iata_code,
            "date_from": tomorrow,
            "date_to": day_in_six_months,
            "curr": "GBP",
            "limit": 1,
            "flight_type": "round",
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "one_for_city": 1,
            "max_stopovers": 7
        }
        response = requests.get(url=f"{TEKILA_BASE_URL}/v2/search", params=request_config, headers=auth_headers)
        response.raise_for_status()
        data = response.json()
        try:
            return data["data"][0]
        except IndexError:
            return None
