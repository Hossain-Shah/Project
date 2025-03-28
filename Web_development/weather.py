import pyowm

owm = pyowm.OWM('94107525c900a1c974d17763794d041a')
observation = owm.weather_at_place("Dhaka,bd")
w = observation.get_weather()
temperature = w.get_temperature('celsius')
tomorrow = pyowm.timeutils.tomorrow()
wind = w.get_wind()
print(w)
print(wind)
print(temperature)
print(tomorrow)