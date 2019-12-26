#! WeatherNotify.py

##################################################
## Script to leverage Accuweather API and use
## Twilio SMS to send weather to individuals.
##################################################
## Author: Fizgriz(Jefffrey Meigs)
## Version: 1.0.0
## Maintainer: Fizgriz(Jeffrey Meigs)
##################################################

# Built-in/Generic Imports
import os
import argparse # Accept runtime switches

# Libs
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from twilio.rest import Client
from dotenv import load_dotenv

parser = argparse.ArgumentParser(description=None)
parser.add_argument('--skipinput', action='store_true',
                    help='skip user input and use default settings')
# Load .env resource
load_dotenv()

# Declare and set variables
## Accuweather API
aw_key = os.getenv("AW_KEY")
aw_url = "http://dataservice.accuweather.com"
## Twilio SMS API
twilio_key = os.getenv("TWILIO_KEY")
twilio_sid = os.getenv("TWILIO_SID")
numbers = os.getenv("SMS_NUMBERS")

def get_location(zipcode):
    """
    get accuweather location id based on Zipcode

    :param zipcode: Zipcode of location.
    :return: returns the accuweather location id.
    """
    loc_id = get(f"""\
            {aw_url}/locations/v1/search?q={zipcode}&apikey={aw_key}
             """).json()
    loc_id = loc_id[0]['Key']

    return loc_id

def get_weather(loc_id,type='both'):
    """
    fetches accuweather json payload as result of weather check.

    :param loc_id: accuweather location id.
    :param type: type of weather to check for(current,forecast).
    defaults to both.

    :return: returns a formatted result.
    """
    if type == 'current':
        payload = get(f"""\
                    {aw_url}/currentconditions/v1/{loc_id}?apikey={aw_key}\
                    """).json()
    elif type == 'forecast':
        payload = get(f"""\
                   {aw_url}/forecasts/v1/daily/1day/{loc_id}?apikey={aw_key}\
                   """).json()
    elif type == 'both':
        payload = get(f"""\
                   {aw_url}/currentconditions/v1/{loc_id}?apikey={aw_key}\
                   """).json()
        payload2 = get(f"""\
                   {aw_url}/forecasts/v1/daily/1day/{loc_id}?apikey={aw_key}\
                   """).json()
    else:
        print("Incorrect choice in method get_weather")
        quit()
    if type == 'both':
        weather = format_weather(type,payload,payload2)
    else:
        weather = format_weather(type,payload)
    return weather

def format_weather(type, payload, payload2=''):
    """
    Formats accuweather result json into reabable string.

    :param type: The type of request it was(current,forecast,both)
    :param payload: The accuweather json payload.
    :param payload2: OPTIONAL, if request type was both.

    :return: returns formatted string for weather.
    """
    if type == 'current':
        for node in payload:
            weather = """The Current weather is {0}F.
                      """.format(node['Temperature']['Imperial']['Value'])
    elif type == 'forecast':
        weather = ("The forecast is a low of {0}F"
                   " a high of {1}F, and today will be {2}."
                   ).format(
                   payload['DailyForecasts'][0]['Temperature']['Minimum']['Value'],
                   payload['DailyForecasts'][0]['Temperature']['Maximum']['Value'],
                   payload['DailyForecasts'][0]['Day']['IconPhrase'])
    elif type == 'both':
        for node in payload:
            weather = ("The Current weather is {0}F."
                       "The forecast is a low of {1}F"
                       " a high of {1}F, and today will be {2}."
                       ).format(
                       node['Temperature']['Imperial']['Value'],
                       payload2['DailyForecasts'][0]['Temperature']['Minimum']['Value'],
                       payload2['DailyForecasts'][0]['Temperature']['Maximum']['Value'],
                       payload2['DailyForecasts'][0]['Day']['IconPhrase'])
    return weather

def send_sms(weather):
    """
    Sends SMS message using twilio SMS API

    :param weather: the weather in formatted string.

    :return: None
    """
    twilio = Client(twilio_sid, twilio_key)
    for number in numbers:
        message = twilio.messages.create(
                                  from_='+1'+os.getenv("SMS_SENDER"),
                                  body=weather,
                                  to='+1'+number
                              )

# Main run
if parser.parse_args().skipinput == False:
    zipcode = input("Enter Zipcode you wish to check for weather: \n")
    type = input("Would you like the [forecast] or [current] weather? \n")
else:
    zipcode = os.getenv('ZIPCODE')
    type = "both"

loc_id = get_location(zipcode)
weather = get_weather(loc_id, type)
send_sms(weather)
print(weather)
