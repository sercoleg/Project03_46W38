import glob
import xarray as xr
import numpy as np

class ERA5Data:
    """ Load and process ERA5 reanalysis data."""

    def __init__(self, data_dir):
        self.data_dir = data_dir

        # extract and sort filenames
        files = sorted(glob.glob(f"{data_dir}/*.nc"))
        # open and save datasets
        datasets = [xr.open_dataset(file) for file in files]
        # concatenate data in datasets using time dimension
        self.data = xr.concat(datasets, dim="time")

    def interpolate(self, latitude, longitude):
        """Interpolate ERA5 data at a given location."""

        point = self.data.interp(latitude=latitude, longitude=longitude)

        return point

def uv_to_speed_direction(u,v):
    """ Convert wind components u and v to wind speed and wind meteorological
    direction."""

    speed = np.sqrt(u**2 + v**2)
    direction = (270 - np.degrees(np.arctan2(v, u))) % 360

    # Fix new variables names and units
    speed.name = "wind_speed"
    speed.attrs["units"] = "m s**-1"

    direction.name = "wind_direction"
    direction.attrs["units"] = "degrees"

    return speed, direction
