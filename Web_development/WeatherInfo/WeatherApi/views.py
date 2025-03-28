from django.shortcuts import render
import requests


def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=94107525c900a1c974d17763794d041a'
    city = 'Dhaka'
    city_weather = requests.get(url.format(city)).json()
    weather = {
        'city': city,
        'temperature': city_weather['main']['temp'],
        'description': city_weather['weather'][0]['description'],
        'icon': city_weather['weather'][0]['icon']
    }
    context = {'weather' : weather}

    return render(request, 'WeatherApi/index.html', context)
