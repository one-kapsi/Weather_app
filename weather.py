import os
import argparse
import requests
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("WEATHER_API_KEY")

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--city", help="Enter City name to get weather for today - by default it is 'Cracow'", default="Cracow")
args = parser.parse_args()

city = args.city
url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}?unitGroup=metric&key={api_key}&contentType=json"

print(f"Getting weather data for {city}")
response = requests.get(url)
print(f"Status code: {response.status_code}")
data = response.json() #this is the sack with all metadata for the next 15 days, it contains absoluutely eveyrything - from here I will be extracting itmes I want
days = data.get("days") # this is list of days from "data" variable
current = data.get("description") # description of the weather conditions for the location - generic from the "data" variable
temperature = days[0]["temp"] # days[0] means today - I want to know whether for current day hence [0]
feels_like = days[0]["feelslike"] # feels like temp for current day
date = days[0]["datetime"] # here I want to print for which date Iam pulling data so again I go to current day and extract datetime - otherwise system doesnt know which day I am asking and pulls everything again

address = data.get("resolvedAddress") # this is addres from the data for the city I am calling at the beginning

print(f"-- Pogoda dla {address} dla dnia {date} -- ")
print(f"Temperatura: {temperature}, odczuwalna: {feels_like}")
print(f"Warunki: {current}")
print("--"*20)
