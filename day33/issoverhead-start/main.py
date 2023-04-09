import time

import requests
from datetime import datetime
import smtplib

MY_LAT = -34.615940 # Your latitude
MY_LONG = -58.433449  # Your longitude

PASSWORD = ""


def request_iss_position():
    global iss_longitude, iss_latitude
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])


#Your position is within +5 or -5 degrees of the ISS position.
def iss_above():
    global iss_longitude, iss_latitude
    request_iss_position()
    print(f"ISS is above? {iss_longitude-5 < MY_LONG < iss_longitude+5 and iss_latitude-5 < MY_LAT < iss_latitude+5}")
    return iss_longitude-5 < MY_LONG < iss_longitude+5 and iss_latitude-5 < MY_LAT < iss_latitude+5


parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}


def request_today_sunset_sunrise():
    global sunrise, sunset
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])


#If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.
def is_dark():
    global sunrise, sunset
    time_now = datetime.now()
    hour_now = time_now.hour
    print("It is dark? ", not (sunrise <= hour_now <= sunset))
    return not (sunrise <= hour_now <= sunset)


def send_mail(msg, subject, to):
    print(f"Sending email: {subject} to {to}")
    my_email = "melhem.developer@gmail.com"
    my_password = PASSWORD
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()  # Encript email (tunnel)
        connection.login(user=my_email, password=my_password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=to,
            msg=f"Subject:{subject}\n\n{msg}")


day = None
iss_latitude = None


def cron_job():
    global iss_latitude, iss_longitude, sunrise, sunset, day
    # Check if day has changed to request sunrise and sunset
    if day != datetime.now().day:
        request_today_sunset_sunrise()
        day = datetime.now().day
    if is_dark() and iss_above():
        send_mail(to="luciano.developer@yahoo.com", msg="Iss is above! watch up!", subject="ISS ABOVE")
    else:
        print(f"Running cron_job, iss is NOT visible")
    time.sleep(60)
    cron_job()


# Run script
cron_job()
