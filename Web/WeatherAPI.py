# importing requests and json
import requests, json, pyowm

from pyowm.owm import OWM
from datetime import datetime, timedelta, timezone


# base URL
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"

CITY = "Dhaka"
API_key = "b5f2851ca9083d63f4eed844c79466a3"


# updating the URL
URL = BASE_URL + "q=" + CITY + "&appid=" + API_key

# HTTP request
response = requests.get(URL)

# checking the status code of the request
if response.status_code == 200:
   # getting data in the json format
   data = response.json()
   # getting the main dict block
   main = data['main']
   # getting temperature
   temperature = main['temp']
   # getting the humidity
   humidity = main['humidity']
   # getting the pressure
   pressure = main['pressure']
   # weather report
   report = data['weather']
   print(f"{CITY:-^30}")
   print(f"Temperature: {temperature}")
   print(f"Humidity: {humidity}")
   print(f"Pressure: {pressure}")
   print(f"Weather Report: {report[0]['description']}")
else:
   # showing the error message
   print("Error in the HTTP request")


owm_obj = OWM(API_key)
mgr = owm_obj.weather_manager()
observation = mgr.weather_at_place('Dhaka,BD') # the observation object is a box
weather = observation.weather
print(weather.detailed_status)
temperature_celsius = weather.temperature('celsius')
print(temperature_celsius)
wind_in_meters_per_sec = weather.wind()
print(wind_in_meters_per_sec)
rain = weather.rain
print(rain)
pressure = weather.pressure
print(pressure['press'])
print(pressure['sea_level'])

registry = owm_obj.city_id_registry()
list_of_locations = registry.locations_for('Dhaka', country='BD')
Dhaka = list_of_locations[0]
lat = Dhaka.lat
lon = Dhaka.lon
one_call = mgr.one_call(lat, lon)
One_call = one_call.forecast_daily[0].temperature('celsius')
print(One_call)
three_days_ago_epoch = int((datetime.now() - timedelta(days=3)).replace(tzinfo=timezone.utc).timestamp())
one_call_three_days_ago_epoch = mgr.one_call_history(lat=52.5244, lon=13.4105, dt=three_days_ago_epoch)
list_of_forecasted_weathers = one_call_three_days_ago_epoch.forecast_hourly
print(list_of_forecasted_weathers)
