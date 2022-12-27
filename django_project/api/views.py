from django.shortcuts import render
from api.models import Weather
from django.http import JsonResponse
import ast
import logging


# Functions
def fetch_weather_data():
    home_dir = '/django_project/'
    source_file = 'current_weather.txt'
    target_file = 'processed_weather_data.txt'

    # Temporary method, can remove once all data is formatted correctly
    with open(f'{home_dir}{source_file}', 'r') as source:
        data = source.read()
        data = data.replace("}{", "}\n{")

    # Write new file to iterate through
    with open(f'{home_dir}{target_file}', 'w') as target:
        target.write(data)

    # Commit appropriate data to database model
    with open(f'{home_dir}{target_file}', 'r') as target:
        for line in target:
            record = ast.literal_eval(line)
            rec = Weather()
            rec.type = record["weather"][0]["main"]
            rec.description = record["weather"][0]["description"]
            rec.temperature = record["main"]["temp"]
            rec.feels_like = record["main"]["temp"]
            rec.temp_min = record["main"]["feels_like"]
            rec.temp_max = record["main"]["temp_min"]
            rec.pressure = record["main"]["temp_max"]
            rec.humidity = record["main"]["pressure"]

            try:
                rec.sea_level_pressure = record["main"]["sea_level"]
            except KeyError:
                rec.sea_level_pressure = 0

            try:
                rec.ground_level_press = record["main"]["grnd_level"]
            except KeyError:
                rec.ground_level_press = 0

            rec.visibility = record["visibility"]
            rec.wind_speed = record["wind"]["speed"]
            rec.wind_degree = record["wind"]["deg"]

            try:
                rec.wind_gust = record["wind"]["gust"]
            except KeyError:
                rec.wind_gust = 0

            try:
                rec.rain_volume = record["rain"]["1h"]
            except KeyError:
                rec.rain_volume = 0

            try:
                rec.snow_volume = record["snow"]["1h"]
            except KeyError:
                rec.snow_volume = 0

            rec.cloud_percent = record["clouds"]["all"]
            rec.collected_unix_time = record["dt"]
            rec.sunrise = record["sys"]["sunrise"]
            rec.sunset = record["sys"]["sunset"]
            rec.city = record["name"]

            """ Commit data to database model """
            try:
                rec.save()
            except:
                logging.warning("Duplicate record detected")

# Create your views here.
def index(request):
    fetch_weather_data()
    weather_values = list(Weather.objects.all().values())
    data = {
        'weather_values': weather_values,
    }

    return JsonResponse(data)