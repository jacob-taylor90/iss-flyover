import requests
from datetime import datetime
import smtplib
import os

MY_LAT = float(os.environ["LATITUDE"])
MY_LNG = float(os.environ["LONGITUDE"])
EMAIL = os.environ["SMTP_EMAIL"]
PASSWORD = os.environ["SMTP_APP_PASSWORD"]

def is_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()

    data = response.json()

    iss_longitude = float(data['iss_position']['longitude'])
    iss_latitude = float(data['iss_position']['latitude'])

    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LNG - 5 <= iss_longitude <= MY_LNG + 5:
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

    sunrise = datetime.fromisoformat(
        data["sunrise"].replace("Z", "+00:00")
    )
    sunset = datetime.fromisoformat(
        data["sunset"].replace("Z", "+00:00")
    )

    time_now = datetime.now(sunrise.tzinfo)

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