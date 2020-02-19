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
    experiment_choices = options.experiments
    ensemble_choices = options.ensembles
    variable_choices = options.variables

    parser.add_argument(
        "-m",
        "--model",
        nargs=1,
        type=str,
        choices=model_choices,
        required=True,
        help=f"Institue and model combination to scan, "
        f"must be one of: {model_choices}",
        metavar="",
    )
    parser.add_argument(
        "-exp",
        "--experiment",
        nargs=1,
        type=str,
        default=experiment_choices,
        required=True,
        help=f"Experiment to scan, " f"must be one of: {experiment_choices}",
        metavar="",
    )
    parser.add_argument(
        "-e",
        "--ensemble",
        nargs=1,
        type=str,
        choices=ensemble_choices,
        required=True,
        help=f"Ensemble to scan, must be one of: " f"{ensemble_choices}",
        metavar="",
    )
    parser.add_argument(
        "-v",
        "--var_id",
        choices=variable_choices,
        default=variable_choices,
        help=f"Variable to scan, can be one or many of: "
        f"{variable_choices}. Default is all variables.",
        metavar="",
        nargs="*",
    )

    return parser.parse_args()


def find_files(model, experiment, ensemble, var_id):
    pattern = (
        "/badc/cmip5/data/cmip5/output1/{model}/{experiment}/mon/land"
        "/Lmon/{ensemble}/latest/{var_id}/*.nc"
    )
    glob_pattern = pattern.format(
        model=model, experiment=experiment, ensemble=ensemble, var_id=var_id
    )
    nc_files = glob.glob(glob_pattern)

    return nc_files


def extract_characteristic(ds, extract_error_path, var_id):

    try:
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

        characteristics = {
            "project_id": project_id,
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
            "time_axis_length": time_axis_length,
        }

        return characteristics

    except Exception as exc:
        if not os.path.exists(extract_error_path):
            os.makedirs(extract_error_path)

        file = open(
            os.path.join(extract_error_path, f"{var_id}.log"), "w"
        )  # creates empty file
        file.write(f"Error extracting characteristics: {exc}")
        return False


def output_to_JSON(
    characteristics, output_path, json_file_name, output_error_path, var_id
):

    # make output directory
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    try:
        # Output to JSON file
        with open(os.path.join(output_path, f"{json_file_name}"), "w") as write_file:
            json.dump(characteristics, write_file, indent=4, sort_keys=True)
        return True

    except Exception as exc:
        if not os.path.exists(output_error_path):
            os.makedirs(output_error_path)

        file = open(
            os.path.join(output_error_path, f"{var_id}.log"), "w"
        )  # creates empty file
        file.write(f"Error outputting to file: {exc}")
        return False


def loop_over_vars(args):
    # keep track of failures
    count = 0
    failure_count = 0

    # turn arguments into string
    model = " ".join(args.model)
    ensemble = " ".join(args.ensemble)
    experiment = " ".join(args.experiment)
    for var_id in args.var_id:
        scanner = scan(model, experiment, ensemble, var_id)
        count += 1
        if scanner is False:
            failure_count += 1
            continue
        else:
            continue

    percentage_failed = (failure_count / count) * 100

    print(
        f"Completed job. Failure count = {failure_count}. Percentage failed = {percentage_failed}"
    )


def scan(model, experiment, ensemble, var_id):

    # get current working directory
    current_directory = os.getcwd()

    # Generate output file path
    output_path = SETTINGS.JSON_OUTPUT_PATH.format(
        current_directory=current_directory,
        model=model,
        ensemble=ensemble,
        experiment=experiment,
    )

    # create directories to log errors, failures and successes
    open_error_path = SETTINGS.OUTPUT_ERROR_PATH.format(
        current_directory=current_directory,
        model=model,
        ensemble=ensemble,
        experiment=experiment,
    )
    success_path = SETTINGS.SUCCESS_PATH.format(
        current_directory=current_directory,
        model=model,
        ensemble=ensemble,
        experiment=experiment,
    )
    no_files_path = SETTINGS.NO_FILES_PATH.format(
        current_directory=current_directory,
        model=model,
        ensemble=ensemble,
        experiment=experiment,
    )
    extract_error_path = SETTINGS.EXTRACT_ERROR_PATH.format(
        current_directory=current_directory,
        model=model,
        ensemble=ensemble,
        experiment=experiment,
    )
    output_error_path = SETTINGS.OUTPUT_ERROR_PATH.format(
        current_directory=current_directory,
        model=model,
        ensemble=ensemble,
        experiment=experiment,
    )

    # check for success file - if exists - continue
    success_file = f"{success_path}/{var_id}.log"

    if os.path.exists(success_file):
        print(
            f"[INFO] Already ran for {model}, {experiment}, {ensemble}, {var_id}."
            " Success file found."
        )
        return

    # delete previous failure files
    no_files_file = f"{no_files_path}/{var_id}.log"
    if os.path.exists(no_files_file):
        os.unlink(no_files_file)

    extract_error_file = f"{extract_error_path}/{var_id}.log"
    if os.path.exists(extract_error_file):
        os.unlink(extract_error_file)

    output_error_file = f"{output_error_path}/{var_id}.log"
    if os.path.exists(output_error_file):
        os.unlink(output_error_file)

    # delete previous log files
    extract_error_file = f"{extract_error_path}/{var_id}.log"
    if os.path.exists(extract_error_file):
        os.unlink(extract_error_file)

    # get files
    nc_files = find_files(model, experiment, ensemble, var_id)

    if not nc_files:

        if not os.path.exists(no_files_path):
            os.makedirs(no_files_path)
        open(os.path.join(no_files_path, f"{var_id}.log"), "w")  # creates empty file

        return False

    # open files
    ds = xr.open_mfdataset(nc_files)

    # create error file if can't open datatset
    if not ds:
        if not os.path.exists(open_error_path):
            os.makedirs(open_error_path)

        open(os.path.join(open_error_path, f"{var_id}.log"), "w")  # creates empty file
        return False

    # extract characteristics
    characteristics = extract_characteristic(ds, extract_error_path, var_id)

    # create error file if can't extract characteristic
    if not characteristics:
        return False

    # output to JSON file
    json_file_name = (
        f"cmip5.output1.{model.replace('/', '.')}.{experiment}.mon.land."
        f"Lmon.{ensemble}.latest.{var_id}.json"
    )
    output = output_to_JSON(
        characteristics, output_path, json_file_name, output_error_path, var_id
    )

    # create error file if can't output file
    if not output:
        return False

    # create success file
    if not os.path.exists(success_path):
        os.makedirs(success_path)

    open(os.path.join(success_path, f"{var_id}.log"), "w")


def main():
    """Runs script if called on command line"""

    args = arg_parse()
    loop_over_vars(args)


if __name__ == "__main__":
    main()
