import requests
from datetime import datetime
import smtplib
import os

MY_LAT = os.environ["LATITUDE"]
MY_LNG = os.environ["LONGITUDE"]
EMAIL = os.environ["SMTP_EMAIL"]
PASSWORD = os.environ["SMTP_APP_PASSWORD"]

def is_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()

    data = response.json()

    longitude = float(data['iss_position']['longitude'])
    latitude = float(data['iss_position']['latitude'])

    if MY_LAT - 5 <= longitude <= MY_LAT + 5 and MY_LNG - 5 <= latitude <= MY_LNG + 5:
        return True
    return False


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LNG,
    }

    response = requests.get(url="https://api.sunrise-sunset.org/v2", params=parameters)
    response.raise_for_status()

    data = response.json()

    sunrise = int(data['sunrise'].split('T')[1].split(':')[0])
    sunset = int(data['sunset'].split('T')[1].split(':')[0])

    time_now = datetime.now().hour

    if sunset <= time_now <= sunrise:
        return True
    return False

#Check if ISS is overhead
if is_overhead() and is_night():
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=EMAIL, password=PASSWORD)
        connection.sendmail(from_addr=EMAIL,
                            to_addrs=EMAIL,
                            msg=f"Subject:Look Up!\n\nThe ISS is currently visible from your position!")