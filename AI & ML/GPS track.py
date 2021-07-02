import gpxpy
import matplotlib.pyplot as plt
import datetime
from geopy import distance
from math import sqrt, floor
import numpy as np
import pandas as pd
import chart_studio.plotly as py
import plotly.graph_objs as go
import haversine
gpx_file = open('D:/Pycharm/Program/AI_Stat_ANN/testdata-master/gps_coordinates/gpx/my_run_001.gpx', 'r')
gpx = gpxpy.parse(gpx_file)
len(gpx.tracks)
len(gpx.tracks[0].segments)
len(gpx.tracks[0].segments[0].points)
data = gpx.tracks[0].segments[0].points
start = data[0]
finish = data[-1]
df = pd.DataFrame(columns=['lon', 'lat', 'alt', 'time'])
for point in data:
    df = df.append({'lon': point.longitude, 'lat': point.latitude, 'alt': point.elevation, 'time': point.time}, ignore_index=True)
print(df)
plt.plot(df['lon'], df['lat'])
plt.show()
#plt.plot(df['time'], df['alt'])
_data = [go.Scatter3d(x=df['lon'], y=df['lat'], z=df['alt'], mode='lines')]
#py.iplot(_data)
alt_dif = [0]
time_dif = [0]
dist_vin = [0]
dist_hav = [0]
dist_vin_no_alt = [0]
dist_hav_no_alt = [0]
dist_dif_hav_2d = [0]
dist_dif_vin_2d = [0]
for index in range(len(data)):
    if index == 0:
        pass
    else:
        start = data[index - 1]
        stop = data[index]
        distance_vin_2d = distance.vincenty((start.latitude, start.longitude), (stop.latitude, stop.longitude)).m
        dist_dif_vin_2d.append(distance_vin_2d)
        distance_hav_2d = haversine.haversine((start.latitude, start.longitude), (stop.latitude, stop.longitude)) * 1000
        dist_dif_hav_2d.append(distance_hav_2d)
        dist_vin_no_alt.append(dist_vin_no_alt[-1] + distance_vin_2d)
        dist_hav_no_alt.append(dist_hav_no_alt[-1] + distance_hav_2d)
        alt_d = start.elevation - stop.elevation
        alt_dif.append(alt_d)
        distance_vin_3d = sqrt(distance_vin_2d ** 2 + (alt_d) ** 2)
        distance_hav_3d = sqrt(distance_hav_2d ** 2 + (alt_d) ** 2)
        time_delta = (stop.time - start.time).total_seconds()
        time_dif.append(time_delta)
        dist_vin.append(dist_vin[-1] + distance_vin_3d)
        dist_hav.append(dist_hav[-1] + distance_hav_3d)
df['dis_vin_2d'] = dist_vin_no_alt
df['dist_hav_2d'] = dist_hav_no_alt
df['dis_vin_3d'] = dist_vin
df['dis_hav_3d'] = dist_hav
df['alt_dif'] = alt_dif
df['time_dif'] = time_dif
df['dis_dif_hav_2d'] = dist_dif_hav_2d
df['dis_dif_vin_2d'] = dist_dif_vin_2d
print('Vincenty 2D : ', dist_vin_no_alt[-1])
print('Haversine 2D : ', dist_hav_no_alt[-1])
print('Vincenty 3D : ', dist_vin[-1])
print('Haversine 3D : ', dist_hav[-1])
print('Total Time : ', floor(sum(time_dif)/60), ' min ', int(sum(time_dif) % 60), ' sec ')
df['dist_dif_per_sec'] = df['dis_dif_hav_2d'] / df['time_dif']
for treshold in [0.5, 0.6, 0.7, 0.8, 0.9, 1]:
    print(treshold, 'm', ' : Time:', sum(df[df['dist_dif_per_sec'] < treshold]['time_dif']), ' seconds')
df['spd'] = (df['dis_dif_hav_2d'] / df['time_dif']) * 3.6
df_with_timeout = df[df['dist_dif_per_sec'] > 0.9]
avg_km_h = (sum((df_with_timeout['spd'] * df_with_timeout['time_dif'])) / sum(df_with_timeout['time_dif']))
print(floor(60 / avg_km_h), 'minutes', round(((60 / avg_km_h - floor(60 / avg_km_h))*60), 0), ' seconds')
df['time10s'] = list(map(lambda x: round(x, -1), np.cumsum(df['time_dif'])))
plt.plot(df.groupby(['time10s']).mean()['spd'])
plt.show()


def positive_only(x):
    if x > 0:
        return x
    else:
        return 0


pos_only = list(map(positive_only, df['alt_dif']))
sum(pos_only)
sum(list(map(lambda x: round(x, 0), pos_only)))
