# submarine_position.py

from pyproj import Transformer
import pandas as pd
import numpy as np
import math
import random
# import plotly.express as px

def lla_to_xyz(lat, lon, alt):
    transprojr = Transformer.from_crs(
        "EPSG:4326",
        {"proj": 'geocent', "ellps": 'WGS84', "datum": 'WGS84'}, always_xy=True)
    x, y, z = transprojr.transform(lon, lat, alt, radians=False)
    return x, y, z

def distance_3d(x1, y1, z1, x2, y2, z2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)

def gauss_noisy(x, y, mu=0, sigma=0.1):
    """
    Add Gaussian noise to input data
    """
    x += random.gauss(mu, sigma)
    y += random.gauss(mu, sigma)
    # z += random.gauss(mu, sigma)
    return x, y



def main():
    # UAV and submarine coordinates in (lat, lon, alt) format
    uav_lla = (18.01944, 112.5194, 300)
    sub_lla = (18.01940, 112.5174, -100) # (18.01944, 112.5184, -100)


    print("Submarine position with added Gaussian noise:", gauss_noisy(sub_lla[0], sub_lla[1]))

if __name__ == "__main__":
    main()