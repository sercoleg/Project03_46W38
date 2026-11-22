import glob
import xarray as xr

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
