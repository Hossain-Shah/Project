from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import folium
from geopy.distance import great_circle
kolkata = (22.5726, 88.3639)
Dhaka = (23.76327225,90.3598240238032)
locator = Nominatim(user_agent="myGeocoder",timeout=4)
location = locator.geocode("Mohammadpur, Dhaka, Bangladesh")
print("Latitude = {}, Longitude = {}".format(location.latitude, location.longitude))
geocode = RateLimiter(locator.geocode, min_delay_seconds=1)
map_osm = folium.Map(location=[23.76327225,90.3598240238032],tiles='cartodbpositron',zoom_start=12)
map_osm.save('osm.html')
print(great_circle(kolkata,Dhaka).km)


