import numpy as np
import pandas as pd
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
import geojsoncontour
import json

# get the winnowed csv with minimum temps
df = pd.read_csv('gsoy_filtered.csv')

lon = df['LONGITUDE'].to_numpy()
lat = df['LATITUDE'].to_numpy()
emnt = df['EMNT'].to_numpy()


# Create a contour plot plot from grid (lat, lon) data
grid_res = 200

x = np.linspace(lon.min(), lon.max(), grid_res)
y = np.linspace(lat.min(), lat.max(), grid_res)
xx, yy = np.meshgrid(x, y)

emnt2 = griddata(
    (lon, lat),
    emnt,
    (xx[None,:], yy[:,None]),
    method='linear'
    )

figure = plt.figure()
ax = figure.add_subplot(111)
contourf = ax.contourf(xx, yy, emnt2[:,0,:])

# Convert matplotlib contour to geojson
geojson = geojsoncontour.contourf_to_geojson(
    contourf=contourf,
    min_angle_deg=3.0,
    ndigits=3,
    stroke_width=2,
    fill_opacity=0.5
)

with open('hardiness_contourf.geojson', 'w') as outfile:
    outfile.write(geojson)

#plt.show()