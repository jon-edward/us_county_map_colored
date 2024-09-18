import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import RBFInterpolator
from shapely import Polygon


bottom_left = np.array([-130, 22])
top_right = np.array([-60, 50])

num_points = 100

seed = 404

rng = np.random.default_rng(seed)

# 2D array of x-y coordinates for points.
points = rng.random((num_points, 2)) * (top_right - bottom_left) + bottom_left

# array of weights for points
values = rng.random((num_points,))

rbf = RBFInterpolator(points, values, kernel="linear")


def bin_interpolation(geometry: Polygon) -> float:
    centroid = geometry.centroid
    return rbf(np.array([[centroid.x, centroid.y]]))[0]


if __name__ == '__main__':
    # Taken from https://catalog.data.gov/dataset/tiger-line-shapefile-2019-nation-u-s-current-county-and-equivalent-national-shapefile
    gdf = gpd.read_file("./tl_2019_us_county.zip")

    gdf["interp_values"] = gdf["geometry"].apply(bin_interpolation)

    ax = gdf.plot(column="interp_values", cmap="inferno")
    ax.set_axis_off()

    plt.xlim([bottom_left[0], top_right[0]])
    plt.ylim([bottom_left[1], top_right[1]])
    plt.savefig("./figure.jpg", dpi=1000, bbox_inches='tight', pad_inches=0.1)
