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

        # get values
        values = ds[var_id].values
        lat_values = ds.lat.values
        lon_values = ds.lon.values
        start_time = ds.time.values[0]
        end_time = ds.time.values[-1]

        # get info about dataset
        project_id = ds.project_id
        institute_id = ds.institute_id
        model_id = ds.model_id
        experiment_id = ds.experiment_id
        frequency = ds.frequency
        modelling_realm = ds.modeling_realm
        # table_id = ds.table_id
        parent_experiment_rip = ds.parent_experiment_rip
        # version = ds.version --> extract from file path (maybe
        # do the same for the one above as well

        # extract characteristics
        # dims = ds.dims
        calendar = ds.time.values[0].calendar
        max_value = str(np.max(values))
        min_value = str(np.min(values))
        units = ds[var_id].units
        standard_name = ds[var_id].standard_name
        long_name = ds[var_id].long_name
        # vars = ds.data_vars
        coords = str(ds.coords._names)
        lat_max = str(np.max(lat_values))
        lat_min = str(np.min(lat_values))
        lon_max = str(np.max(lon_values))
        lon_min = str(np.min(lon_values))
        time_long_name = ds.time.long_name
        time_standard_name = ds.time.standard_name
        # coord_values
        shape = ds[var_id].shape
        # rank = ds.rank
        start_date = start_time.strftime("%Y-%m-%d %H:%M:%S")
        end_date = end_time.strftime("%Y-%m-%d %H:%M:%S")
        time_axis_length = len(ds.time)
        # fill_value =

        # Generate file path
        output_path = f"/home/users/esmith88/roocs/character_scanner/outputs/cmip5/output1/MOHC/" \
                      f"HadGEM2-ES/r1i1p1"

        if os.path.exists(output_path):
            pass
        else:
            os.makedirs(output_path)

        # Output to JSON file
        with open(os.path.join(output_path, f"cmip5.output1.MOHC.HadGEM2-ES.historical.mon.land.Lmon.r1i1p1.latest.{var_id}.json"), "w") as write_file:
            json.dump({"project_id": project_id,
                       "institute_id": institute_id,
                       "model_id": model_id,
                       "experiment_id": experiment_id,
                       "frequency": frequency,
                       "modelling_realm": modelling_realm,
                       "parent_experiment_rip": parent_experiment_rip,
                       "variable": var_id,
                       "calendar": calendar,
                       "max_value": max_value,
                       "min_value": min_value,
                       "units": units,
                       "standard_name": standard_name,
                       "long_name": long_name,
                       "coords": coords,
                       "lat_max": lat_max,
                       "lat_min": lat_min,
                       "lon_max": lon_max,
                       "lon_min": lon_min,
                       "time_long_name": time_long_name,
                       "time_standard_name": time_standard_name,
                       "shape": shape,
                       "start_date": start_date,
                       "end_date": end_date,
                       "time_axis_length": time_axis_length
                       },
                        write_file, indent=4)


def main():
    """Runs script if called on command line"""
    open_files()
    


if __name__ == '__main__':
    main()