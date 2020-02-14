#!/usr/bin/env python

import json
import glob
import os
import xarray as xr
import numpy as np

from lib import variables

def find_files(var_id):
    """
    Finds files that correspond to the given arguments.

    :param var_id: (string) Variable given as argument from for loop.
    :return: The netCDF files that correspond to the arguments.
    """

    pattern = '/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/historical/mon/land' \
              '/Lmon/r1i1p1/latest/{var_id}/*.nc'
    glob_pattern = pattern.format(var_id=var_id)
    nc_files = glob.glob(glob_pattern)
    # print(f'[INFO] found files: {nc_files}')

    return nc_files

def open_files():

    #for var_id in variables.variables:
    for var_id in range(1):
        var_id = 'rh'
        nc_files = find_files(var_id)

        # open files
        ds = xr.open_mfdataset(nc_files)

        # extract characteristics

        # dims = ds.dims
        # calendar = ds.dt.year
        max_value = str(np.max(ds[var_id].values))
        min_value = str(np.min(ds[var_id].values))
        units = ds[var_id].units
        standard_name = ds[var_id].standard_name
        long_name = ds[var_id].long_name
        # vars = ds.data_vars
        # coords = ds.coords
        lat_max = str(np.max(ds.lat.values))
        lat_min = str(np.min(ds.lat.values))
        lon_max = str(np.max(ds.lon.values))
        lon_min = str(np.min(ds.lon.values))
        time_long_name = ds.time.long_name
        time_standard_name = ds.time.standard_name
        # coord_values
        shape = ds[var_id].shape
        # rank = ds.rank
        start_date = ds.time[0]
        print(start_date)
        # end_date
        # time_length

        





        output_path = f"/home/users/esmith88/roocs/character_scanner/outputs/cmip5/output1/MOHC/" \
                      f"HadGEM2-ES/historical/r1i1p1"

        if os.path.exists(output_path):
            pass
        else:
            os.makedirs(output_path)

        # output to JSON file

        with open(os.path.join(output_path, f"cmip5.output1.MOHC.HadGEM2-ES.r1i1p1.{var_id}.json"), "w") as write_file:
            json.dump({"variable": var_id,
                       "max_value": max_value,
                       "min_value": min_value,
                       "standard_name": standard_name,
                       "long_name": long_name,
                       "units": units,
                       "lat_max": lat_max,
                       "lat_min": lat_min,
                       "lon_max": lon_max,
                       "lon_min": lon_min,
                       "time_long_name": time_long_name,
                       "time_standard_name": time_standard_name,
                       "shape": shape,

                       },
                        write_file)


def main():
    """Runs script if called on command line"""
    open_files()
    


if __name__ == '__main__':
    main()