import os
import requests
from dotenv import load_dotenv
from initial_data import flights_initial

load_dotenv()


class DataManager:
    # This class is responsible for talking to the Google Sheet.

    def get_low_prices_sheet(self):
        auth_headers = {
            "Authorization": os.environ["SHEETY_AUTH_TOKEN"]
        }
        response = requests.get(url=os.environ["SHEETY_GET_URL"], headers=auth_headers)
        response.raise_for_status()
        data = response.json()
        print(data)
        return data

    def parse_initial_data(self):
        data = flights_initial["flights"]
        return data

    def update_iata_code(self, row):
        auth_headers = {
            "Authorization": os.environ["SHEETY_AUTH_TOKEN"]
        }
        request_config ={
            "flight": row
        }
        response = requests.put(url=f"{os.environ['SHEETY_PUT']}{row['id']}", json=request_config, headers=auth_headers)
        response.raise_for_status()
