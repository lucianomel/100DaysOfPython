import requests
from datetime import datetime
# response = requests.get(url="http://api.open-notify.org/iss-now.json")
#
# # if response.status_code == 404:
# #     raise Exception("That resource does not exist")
# # elif response.status_code == 401:
# #     raise Exception("Not authorized")
# # Raise error
# response.raise_for_status()
#
# data = response.json()
# longitude = data["iss_position"]["longitude"]
# latitude = data["iss_position"]["latitude"]
#
# iss_position = (longitude,latitude)
#
# print(iss_position)
#

LATITUDE = -34.615940
LONGITUDE = -58.433449

parameters = {
    "lat":LATITUDE,
    "lng":LONGITUDE,
    "formatted":0
}

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = data["results"]["sunrise"].split("T")[1].split(":")[0]
sunset = data["results"]["sunset"].split("T")[1].split(":")[0]

print(sunrise)
print(sunset)

time_now = datetime.now()

print(time_now.hour)