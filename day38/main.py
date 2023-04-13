import os
from datetime import datetime
import requests


def nutritionix_nlp(user_input):
    natural_language_exercise_endpoint = f"{os.environ.get('NUTRITIONIX_BASE_URL')}v2/natural/exercise"
    query_config = {
        "query": user_input,
        "gender": "male",
        "weight_kg": 88,
        "height_cm": 190,
        "age": 26
    }
    auth_headers = {
        "x-app-id": os.environ.get("NUTRITIONIX_APP_ID"),
        "x-app-key": os.environ.get("NUTRITIONIX_API_KEY"),
        "x-remote-user-id": "0"
    }
    response = requests.post(url=natural_language_exercise_endpoint, json=query_config, headers=auth_headers)
    response.raise_for_status()
    data = response.json()
    return data


def parse_data(data, worksheet_name):
    parsed_data = []
    time = datetime.now().strftime("%H:%M:%S")
    date = datetime.now().strftime("%d/%m/%Y")
    for exercise in data["exercises"]:
        calories = exercise['nf_calories']
        duration = exercise['duration_min']
        exercise = exercise['name']
        parsed_data.append({
            worksheet_name: {
                'calories': str(calories),
                'duration': str(duration),
                'exercise': exercise,
                'time': time,
                'date': date
            }
        })
    return parsed_data


def sheety_post(parsed_data):
    sheety_post_headers = {
        "Authorization": os.environ.get("SHEETY_AUTHORIZATION")
    }
    for data in parsed_data:
        response = requests.post(url=os.environ.get("SHEETY_POST_URL"), json=data, headers=sheety_post_headers)
        response.raise_for_status()


def write_sheet(sheet):
    user_input = input("Tell me what exercises you did: ")
    data = nutritionix_nlp(user_input)
    parsed_data = parse_data(data, sheet)

    sheety_post(parsed_data)


write_sheet('workout')
