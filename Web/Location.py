import geocoder
import folium
g = geocoder.ip('me')
print(g)
print(g.latlng)
my_map1 = folium.Map(location=g.latlng, zoom_start=12)
folium.Marker(g.latlng, popup=' Current Location ').add_to(my_map1)
print(my_map1)
my_map1.save('MyLocation.html')
