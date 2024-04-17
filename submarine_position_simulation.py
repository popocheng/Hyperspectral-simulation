# submarine_position.py

from pyproj import Transformer
import pandas as pd
import numpy as np
import math
import random
import plotly.express as px

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

    # Convert (lat, lon, alt) to (x, y, z)
    uav_x, uav_y, uav_z = lla_to_xyz(uav_lla[0], uav_lla[1], uav_lla[2])
    sub_x, sub_y, sub_z = lla_to_xyz(sub_lla[0], sub_lla[1], sub_lla[2])

    # Read submarine shape simulation data and hyperspectral background data
    df = pd.read_csv('df_im_sub.csv')
    im_sub = np.array(df)

    df_ = pd.read_csv('df_noise.csv')
    noi = np.array(df_)

    # Calculate 3D distance between submarine and UAV
    L_sub_uav = distance_3d(sub_x, sub_y, sub_z, uav_x, uav_y, uav_z)

    # Calculate distance from submarine to the center of view based on hypotenuse and height
    d = math.sqrt(L_sub_uav**2 - (uav_lla[2] - sub_lla[2])**2)

    # Detection range (radius)
    D = 1000

    # Check if the distance d exceeds the detection range
    if d > D:
        print('Submarine is out of detection range')
    else:
        # Add submarine shape to background noise at the specified position
        noi = noi * 10
        noi[100 + int(d / 13.8) - 40:100 + int(d / 13.8), 100 + int(d / 13.8) - 60:100 + int(d / 13.8)] = im_sub

    # Visualize submarine position simulation using Plotly
    cls = px.imshow(noi, color_continuous_scale='jet')
    cls.update_layout(title='Submarine Position Simulation', coloraxis_showscale=True)
    cls.update_xaxes(showticklabels=False)
    cls.update_yaxes(showticklabels=False)
    cls.write_image('submarine_position_simulation.png')
    cls.show()

    # Return submarine position information with added Gaussian noise
    print("Submarine position with added Gaussian noise:", gauss_noisy(sub_lla[0], sub_lla[1]))

if __name__ == "__main__":
    main()