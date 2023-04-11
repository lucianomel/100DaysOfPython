import random
import string

import requests
from uuid import uuid4
from datetime import datetime
import pandas as pd
pixela_endpoint = "https://pixe.la/v1/users"


def user_exists(user):
    try:
        users_df = pd.read_csv("users.csv", index_col=0)
    except FileNotFoundError:
        return False
    else:
        stored_data = users_df[users_df["username"] == user]
        return not stored_data.empty


class HabitTracker:
    def __init__(self):
        self.username = None
        self.token = None
        self.graphs = []

    def save_token_in_file(self):
        """Creates persistent data for login"""
        try:
            df = pd.read_csv("users.csv", index_col=0)
        except FileNotFoundError:
            df = pd.DataFrame([[self.username, self.token]], columns=["username", "token"])
            df.to_csv("users.csv")
        else:
            df2 = pd.DataFrame([[self.username, self.token]],
                               columns=['username', 'token'])
            pd.concat([df, df2], ignore_index=True).to_csv("users.csv")

    def sign_up(self, input_username):
        """Creates a user and logs in"""
        # Login:
        self.username = input_username
        self.token = str(uuid4())
        # API call to generate user
        user_params = {
            "token": self.token,
            "username": self.username,
            "agreeTermsOfService": "yes",
            "notMinor": "yes"
        }
        try:
            response = requests.post(url=pixela_endpoint, json=user_params)
            response.raise_for_status()
            print(response.text)
            # Persistent data
            self.save_token_in_file()
            return {"error": None, "response": response, "token": self.token}
        except requests.exceptions.HTTPError as e:
            return {"error": e, "response": None}

    def login(self, username):
        users_df = pd.read_csv("users.csv", index_col=0)
        stored_data = users_df[users_df["username"] == username]
        if stored_data.empty:
            return {"error": "No user found"}
        else:
            user_and_token = stored_data.iloc[0]
            # Login:
            self.username = user_and_token.username
            self.token = user_and_token.token
            return {"msg": f"Login successful {self.username}, {self.token}"}

    def get_auth_headers(self):
        return {"X-USER-TOKEN": self.token}

    def create_graph(self, graph_name, graph_units, graph_type, graph_color="kuro"):
        """API call. Create a graph under the current user. Graph type refers to the data type for the pixels of the
         graph (int/float). Returns a dictionary with graph_id attribute if successful (only if logged in). Default
         color is black"""
        graph_endpoint = f"{pixela_endpoint}/{self.username}/graphs"

        graph_id = ''.join(random.choices(string.ascii_letters.lower() + string.digits, k=16))
        graph_config = {
            "id": graph_id,
            "name": graph_name,
            "unit": graph_units,
            "type": graph_type,
            "color": graph_color
        }
        while True:
            try:
                response = requests.post(url=graph_endpoint, json=graph_config, headers=self.get_auth_headers())
                response.raise_for_status()
                self.graphs.append(graph_config)
                return {"error": None, "response": response, "graph_id": graph_id}
            except requests.exceptions.HTTPError as e:
                print({"error": e, "response": None})

    def add_pixel_today(self, graph_id, qty):
        """Api call. Graph id should be an id of a already created graph (only if logged in)"""
        post_pixel_endpoint = f"{pixela_endpoint}/{self.username}/graphs/{graph_id}"

        today_str = datetime.now().strftime("%Y%m%d")

        post_pixel_config = {
            "date": today_str,
            "quantity": str(qty)
        }
        while True:
            try:
                response = requests.post(url=post_pixel_endpoint, json=post_pixel_config, headers=self.get_auth_headers())
                response.raise_for_status()
                return {"error": None, "response": response}
            except requests.exceptions.HTTPError as e:
                return {"error": e, "response": None}

    def modify_pixel(self, date, graph_id, pixel_qty):
        """Api call. Date in format YYYYmmdd, pixel_qty in defined type for the graph indicated with graph_id
        (only if logged in)"""
        update_pixel_endpoint = f"{pixela_endpoint}/{self.username}/graphs/{graph_id}/{date}"

        update_pixel_config = {
            "quantity": pixel_qty
        }
        try:
            response = requests.put(url=update_pixel_endpoint,
                                    json=update_pixel_config,
                                    headers=self.get_auth_headers())
            response.raise_for_status()
            return {"error": None, "response": response}
        except requests.exceptions.HTTPError as e:
            return {"error": e, "response": None}

    def delete_pixel(self, graph_id, date):
        """Api call to delete a pixel (only if logged in)"""
        delete_pixel_endpoint = f"{pixela_endpoint}/{self.username}/graphs/{graph_id}/{date}"
        try:
            response = requests.delete(url=delete_pixel_endpoint, headers=self.get_auth_headers())
            response.raise_for_status()
            return {"error": None, "response": response}
        except requests.exceptions.HTTPError as e:
            return {"error": e, "response": None}

    def get_graphs(self):
        """Returns graphs array of graphs reference, each reference a dictionary with keys id and name"""
        graphs = []
        for graph in self.graphs:
            graphs.append({"id": graph.id, "name": graph.name})
        return graphs

    def save_graph_img(self, graph_id):
        graph_endpoint = f"{pixela_endpoint}/{self.username}/graphs/{graph_id}"
        try:
            response = requests.get(url=graph_endpoint, headers=self.get_auth_headers())
            response.raise_for_status()
            with open("image.svg", "w") as f:
                f.write(response.text)
            return {"error": None, "response": response, "graph_id": graph_id}
        except requests.exceptions.HTTPError as e:
            return {"error": e, "response": None}
