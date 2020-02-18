#!/usr/bin/env python

import json
import glob
import os
import xarray as xr
import numpy as np
import argparse

import SETTINGS
from lib import options

def arg_parse():
    parser = argparse.ArgumentParser()

    model_choices = options.models
    ensemble_choices = options.ensembles
    variable_choices = options.variables

    parser.add_argument('-m', '--model', nargs=1, type=str, choices=model_choices,
                        required=True, help=f'Institue and model combination to run statistic on, '
                                            f'must be one of: {model_choices}', metavar='')
    parser.add_argument('-e', '--ensemble', nargs=1, type=str, choices=ensemble_choices,
                        required=True, help=f'Ensemble to run statistic on, must be one of: '
                                            f'{ensemble_choices}', metavar='')
    parser.add_argument('-v', '--var_id', choices=variable_choices, default=variable_choices,
                        help=f'Variable to run statistic on, can be one or many of: '
                             f'{variable_choices}. Default is all variables.', metavar='',
                        nargs='*')

    return parser.parse_args()


def find_files(model, ensemble, var_id):
    pattern = '/badc/cmip5/data/cmip5/output1/{model}/historical/mon/land' \
              '/Lmon/{ensemble}/latest/{var_id}/*.nc'
    glob_pattern = pattern.format(model=model, ensemble=ensemble, var_id=var_id)
    nc_files = glob.glob(glob_pattern)

    return nc_files


def loop_over_vars(args):
    # turn arguments into string
    model = ' '.join(args.model)
    ensemble = ' '.join(args.ensemble)
    for var_id in args.var_id:
        make_json(model, ensemble, var_id)


def make_json(model, ensemble, var_id):
    # get current working directory
    current_directory = os.getcwd()  

    print(model, ensemble, var_id)
    # create directory to log errors
    error_log_path = SETTINGS.ERROR_LOG_PATH.format(
        current_directory=current_directory, model=model, ensemble=ensemble)

    # get files
    nc_files = find_files(model, ensemble, var_id)
    
    if not nc_files:

        # if not os.path.exists(error_log_path):
        #     os.makedirs(error_log_path)

        # file = open(os.path.join(error_log_path, f'{var_id}.log'), 'w')  # creates empty file
        #
        # file.write("Files do not exist")
        return False

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
    modeling_realm = ds.modeling_realm
    # table_id = ds.table_id
    parent_experiment_rip = ds.parent_experiment_rip
    # version = ds.version --> extract from file path (maybe
    # do the same for the one above as well)

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
    output_path = SETTINGS.JSON_OUTPUT_PATH.format(
        current_directory=current_directory, model=model, ensemble=ensemble)

    # make output directory
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # change format of institute/model
    model = model.replace('/', '.')

    # Output to JSON file
    with open(os.path.join(output_path, f"cmip5.output1.{model}.historical.mon.land.Lmon.{ensemble}.latest.{var_id}.json"), "w") as write_file:
        json.dump({"project_id": project_id,
                   "institute_id": institute_id,
                   "model_id": model_id,
                   "experiment_id": experiment_id,
                   "frequency": frequency,
                   "modeling_realm": modeling_realm,
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
                  write_file, indent=4, sort_keys=True)


def main():
    """Runs script if called on command line"""
    
    args = arg_parse()
    loop_over_vars(args)
    

if __name__ == '__main__':
    main()