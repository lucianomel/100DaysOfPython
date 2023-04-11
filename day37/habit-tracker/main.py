import os
import requests
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()


pixela_endpoint = "https://pixe.la/v1/users"

# --- CREATE USER --- #

# user_params = {
#     "token": os.environ.get("PIXELA_TOKEN"),
#     "username": os.environ.get("PIXELA_USERNAME"),
#     "agreeTermsOfService": "yes",
#     "notMinor": "yes"
# }

# response = requests.post(url=pixela_endpoint, json=user_params)
# print(response.text)

# ---- CREATE GRAPH ---- #

# graph_endpoint = f"{pixela_endpoint}/{os.environ.get('PIXELA_USERNAME')}/graphs"
#
# graph_config = {
#     "id": "graph2",
#     "name": "Hours coding per day",
#     "unit": "hours",
#     "type": "int",
#     "color": "sora"
# }
#
# headers = {
#     "X-USER-TOKEN": os.environ.get("PIXELA_TOKEN")
# }

# response = requests.post(url=graph_endpoint, json=graph_config, headers=headers)
# print(response.text)

# ---- POST A PIXEL ---- #

graph_id = "graph2"

post_pixel_endpoint = f"{pixela_endpoint}/{os.environ.get('PIXELA_USERNAME')}/graphs/{graph_id}"

today_str = datetime.now().strftime("%Y%m%d")

headers = {
    "X-USER-TOKEN": os.environ.get("PIXELA_TOKEN")
}

post_pixel_config = {
    "date": today_str,
    "quantity": input("How many hours have you coded today? (whole number): ")
}

response = requests.post(url=post_pixel_endpoint, json=post_pixel_config, headers=headers)

print(response.text)

# ---- PUT ----- #

# graph_id = "graph2"
#
# yesterday_str = (datetime.now()+timedelta(days=-1)).strftime("%Y%m%d")
#
# update_pixel_endpoint = f"{pixela_endpoint}/{os.environ.get('PIXELA_USERNAME')}/graphs/{graph_id}/{yesterday_str}"
#
# headers = {
#     "X-USER-TOKEN": os.environ.get("PIXELA_TOKEN")
# }
#
# update_pixel_config = {
#     "quantity": "4"
# }
#
# response = requests.put(url=update_pixel_endpoint, json=update_pixel_config, headers=headers)
#
# print(response.text)

# ---- DELETE ----- #

# graph_id = "graph2"
#
# today_str = datetime.now().strftime("%Y%m%d")
#
# delete_pixel_endpoint = f"{pixela_endpoint}/{os.environ.get('PIXELA_USERNAME')}/graphs/{graph_id}/{today_str}"
#
# headers = {
#     "X-USER-TOKEN": os.environ.get("PIXELA_TOKEN")
# }
#
# response = requests.delete(url=delete_pixel_endpoint, headers=headers)
#
# print(response.text)


