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

    def interpolate(self, latitude, longitude, start_year=1997, end_year=2008):
        """Interpolate ERA5 data at a given location for a period of years."""

        # select period before interpolating
        data_period = self.data.sel(time=slice(str(start_year), str(end_year)))

        point = data_period.interp(latitude=latitude, longitude=longitude)

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

def calculate_shear_exponent(speed10, speed100, min_speed=3,
                             height_low=10, height_high=100):
    """Calculate a representative long-term wind shear exponent based on
    power law."""

    # Exclude low wind speeds from hourly shear calculation
    valid = speed10 >= min_speed

    alpha_hourly = (np.log(speed100 / speed10) /
                    np.log(height_high / height_low)).where(valid)

    alpha_monthly = (alpha_hourly.groupby("time.month").median(skipna=True))

    alpha_long_term = alpha_monthly.mean()

    return alpha_long_term

def power_law(speed_ref, height_ref, height, alpha):
    """Extrapolate wind speed to a target height using the power law."""

    speed_height = speed_ref * (height / height_ref)**alpha

    return speed_height

