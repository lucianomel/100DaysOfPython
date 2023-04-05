import smtplib
import datetime as dt
from random import choice

PASSWORD = ""

def send_mail(msg,subject,to):
    my_email = "melhem.developer@gmail.com"
    my_password = PASSWORD
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls() # Encript email (tunnel)
        connection.login(user=my_email, password=my_password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=to,
            msg=f"Subject:{subject}\n\n{msg}")


def send_mail_today():
    now = dt.datetime.now()
    day_of_week = now.weekday()
    with open("quotes.txt") as quotes_file:
        quotes = quotes_file.readlines()
        random_quote = choice(quotes)
    print(random_quote)
    if day_of_week == 0:
        print("Sending mail...")
        send_mail(msg=random_quote, subject="Weekly Random quote", to="luciano.developer@yahoo.com")


send_mail_today()
