import folium
folium_map = folium.Map(location=[23.76327225,90.3598240238032],
                        zoom_start=13,
                        tiles="CartoDB dark_matter")
marker = folium.CircleMarker(location=[23.76327225,90.3598240238032])
marker.add_to(folium_map)
folium_map.save("my_map.html")
