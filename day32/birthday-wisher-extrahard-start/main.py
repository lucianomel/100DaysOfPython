##################### Extra Hard Starting Project ######################
import pandas as pd
import datetime as dt
import os
from random import choice
import smtplib

# 1. Update the birthdays.csv DONE
PASSWORD = ""

# 2. Check if today matches a birthday in the birthdays.csv
def today_is_birthday(target):
    today = dt.datetime.now()
    today_month = today.month
    today_day = today.day
    return today_day == target.day and today_month == target.month


def send_birthday_emails():
    df_birthdays = pd.read_csv("birthdays.csv")
    for i, entry in df_birthdays.iterrows():
        entry_date = dt.datetime(year=entry["year"], month=entry["month"], day=entry["day"])
        if today_is_birthday(entry_date):
            msg = pick_random_letter_and_replace(entry["name"])
            send_mail(msg=msg, subject="Happy Birthday!", to=entry["email"])


# 3. If step 2 is true, pick a random letter from letter templates and replace the [NAME]
# with the person's actual name from birthdays.csv
def pick_random_letter_and_replace(name):
    filename = choice(os.listdir(f"{os.getcwd()}/letter_templates"))
    with open(os.path.join(f"{os.getcwd()}/letter_templates", filename), 'r') as f:
        msg = f.read()
        msg = msg.replace("[NAME]", name)
    return msg


# 4. Send the letter generated in step 3 to that person's email address.

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


send_birthday_emails()
