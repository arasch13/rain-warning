import os
import requests
from twilio.rest import Client


# insert location here
MY_LAT = 50.735380
MY_LONG = 7.104300


def check_rain(weather_id: str) -> bool:
    if weather_id[0] in ["2", "5", "6"]:
        return True
    else:
        return False


def send_warning_sms():
    account_sid = os.environ["ACC_SID"]
    auth_token = os.environ["AUTH_TOKEN"]
    client = Client(account_sid, auth_token)
    client.messages.create(
        body='Heute gibt es Niederschlag. Nimm besser einen ☂️ mit.',
        from_=os.environ["TWILIO_NUMBER"],
        to=os.environ["MY_MOBILE_NUMBER"]
    )
    print(client.messages)


def rain_warning():
    # send api request and receive one api call data
    parameters = {
        'lat': MY_LAT,
        'lon': MY_LONG,
        'appid': os.environ["APP_ID"],
        'exclude': "current,minutely,daily"
    }
    result = requests.get(
        url="https://api.openweathermap.org/data/2.5/onecall",
        params=parameters
    )
    result.raise_for_status()
    data = result.json()

    # check next 12 hours for thunderstorm, rain or snow
    hourly_data = data['hourly']
    for hour in hourly_data[0:12]:
        weather_id = hour['weather'][0]['id']
        if check_rain(str(weather_id)):
            send_warning_sms()
            break
