import os
import argparse
import requests
import json
import redis
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("WEATHER_API_KEY")
redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True) # link to the DB

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--city", help="Enter City name to get weather for today - by default it is 'Cracow'", default="Cracow")
args = parser.parse_args()

city = args.city
redis_key = (f"weather:{city.lower()}") # this is name of the container in which we will be looking for in DB
cached_data = redis_client.get(redis_key) # this is a response from the DB whether it is there or not based on the container above

url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}?unitGroup=metric&key={api_key}&contentType=json"

print(f"Getting weather data for {city}")

if cached_data:
    print(f"Data for {city} is found in local cache!")
    data = json.loads(cached_data) # here I am loading the weather data to the container for future reference. This contains all metadata for 15 days - absolutely everything 
else:
    print(f"Data for {city} is NOT found in local cache! Calling API")
    response = requests.get(url) # if the city is not found in the DB, then I wil call the API
    print(f"Status code: {response.status_code}")
    data = response.json() #this is the sack with all metadata for the next 15 days, it contains absoluutely eveyrything - from here I will be extracting itmes I want
    redis_client.set(redis_key, json.dumps(data), ex=300)
days = data.get("days") # this is list of days from "data" variable
current = data.get("description") # description of the weather conditions for the location - generic from the "data" variable
temperature = days[0]["temp"] # days[0] means today - I want to know whether for current day hence [0]
feels_like = days[0]["feelslike"] # feels like temp for current day
date = days[0]["datetime"] # here I want to print for which date Iam pulling data so again I go to current day and extract datetime - otherwise system doesnt know which day I am asking and pulls everything again

address = data.get("resolvedAddress") # this is addres from the data for the city I am calling at the beginning

print(f"-- Weather for {address} on {date} -- ")
print(f"Temperature: {temperature}, Feels Like: {feels_like}")
print(f"Current conditions: {current}")
print("--"*20)
