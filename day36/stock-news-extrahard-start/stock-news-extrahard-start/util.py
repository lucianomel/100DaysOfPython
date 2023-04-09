import datetime as dt
import json


def save_api_call(topic, api_caller):
    today = str(dt.datetime.now()).split(" ")[0]
    try:
        with open(f"{topic}_{today}.json", "r") as f:
            news = json.load(f)
            return news
    except FileNotFoundError:  # Api call
        response = api_caller()
        data = response.json()
        data_json = json.dumps(data, indent=4)
        with open(f"{topic}_{today}.json", "w") as f:
            f.write(data_json)
        return data

