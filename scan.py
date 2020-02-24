#!/usr/bin/env python

"""
Takes arguemnts from the command line and scans each dataset to extract the characteristics.
Outputs the characteristics to JSON files.

Can be re-run if errors are fixed and will only run those which failed.
"""

import json
import collections
import os
import argparse

import xarray as xr

import SETTINGS
from .lib import options


def arg_parse():
    """
    Parses arguments given at the command line

    :return: Namespace object built from attributes parsed from command line.
    """
    parser = argparse.ArgumentParser()
    project_options = options.known_projects

    parser.add_argument(
        "-p",
        "--project",
        nargs=1,
        type=str,
        choices=project_options,
        required=True,
        help=f'Project ID, must be one of: {project_options}'
    )

    parser.add_argument(
        "-d",
        "--dataset-ids",
        nargs=1,
        type=str,
        default=None,
        required=False,
        help='List of comma-separated dataset identifiers'
    )

    parser.add_argument(
        "-f",
        "--facets",
        nargs=1,
        type=str,
        default=None,
        required=False,
        help='Set of facets to use, formatted as: x=hello,y=2,z=bye'
    )

    parser.add_argument(
        "-e",
        "--exclude",
        nargs=1,
        type=str,
        default=None,
        required=False,
        help=f'Regular expressions for excluding paths from being scanned'
    )

    return parser.parse_args()


def extract_character(ds, var_id, extract_error_path):
    """
    Takes a dataset and extracts characteristics from it. If a characteristic
    can't be extracted it creates an error file.

    :param ds: (xarray.Dataset) The dataset to extract characteristics from.
    :param var_id: (string) The variable chosen as an argument at the command line.
    :param extract_error_path: (string) The file path at which the error files are produced.
    :return characteristics: (dict) The extracted characteristics. Returned as a dictionary.
    """

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

        table_id = ds.table_id.split(" ")[1]
        realisation = ds.realization
        initialisation_method = ds.initialization_method
        physics_version = ds.physics_version
        ensemble = f"r{realisation}i{initialisation_method}p{physics_version}"

        # extract characteristics
        dims = dict(ds.dims)
        calendar = ds.time.values[0].calendar
        max_value = float(values.max())
        min_value = float(values.min())
        units = ds[var_id].units
        standard_name = ds[var_id].standard_name
        long_name = ds[var_id].long_name
        # vars = ds.data_vars
        coords = str(ds.coords._names)
        lat_max = lat_values.max()
        lat_min = lat_values.min()
        lon_max = lon_values.max()
        lon_min = lon_values.min()
        time_long_name = ds.time.long_name
        time_standard_name = ds.time.standard_name
        shape = ds[var_id].shape
        rank = len(ds.dims)
        start_date = start_time.strftime("%Y-%m-%d %H:%M:%S")
        end_date = end_time.strftime("%Y-%m-%d %H:%M:%S")
        time_axis_length = len(ds.time)
        # fill_value =

        characteristics = {
            "dims": dims,
            "project_id": project_id,
            "institute_id": institute_id,
            "model_id": model_id,
            "experiment_id": experiment_id,
            "ensemble": ensemble,
            "table_id": table_id,
            "frequency": frequency,
            "modeling_realm": modeling_realm,
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
            "rank": rank,
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


def to_json(character, output_path, json_file_name, output_error_path, var_id):
    """
    Outputs the extracted characteristics to a JSON file.
    If the characteristics can't be output an error file is produced.

    :param character: (dict) The extracted characteristics.
    :param output_path: (string) The file path at which the JSON file is produced.
    :param json_file_name: (string) The name of the JSON file to be produced.
    :param output_error_path: (string) The file path at which the error files are produced.
    :param var_id: (string)The variable chosen as an argument at the command line.
    :return : None
    """

    # make output directory
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    try:
        # Output to JSON file
        with open(os.path.join(output_path, json_file_name), "w") as write_file:
            json.dump(characteristics, write_file, indent=4, sort_keys=True)
        return True

    except Exception as exc:
        if not os.path.exists(output_error_path):
            os.makedirs(output_error_path)

        with open(os.path.join(output_error_path, f"{var_id}.log"), "w") as error_file:
            error_file.write(f"Error outputting to file: {exc}")

        print(exc)
        return False


def get_dataset_paths(args):
    """
    Converts the input arguments into an Ordered Dictionary of {DSID: directory} items.

    :param args: (namespace) Namespace object built from attributes parsed from command line
    :return: An Ordered Dictionary of {dsid: directory}
    """
    project = args.project
    ds_ids = args.ds_ids
    paths = args.paths
    facets = dict([_.split(',') for _ in args.facets])
    exclude = args.exclude

    base_dir = options.project_base_dirs(project)
    ds_paths = collections.OrderedDict()

    # If ds_ids is defined then ignore all other arguments and use this list
    if ds_ids:

        for dsid in ds_ids.split(','):
            ds_path = os.path.join(base_dir, '/'.join(dsid.split('.')))
            ds_paths[dsid] = ds_path
    else:
        raise NotImplementedError('Code currently breaks if not using "ds_ids" argument.')

    return ds_paths


def scan_datasets(args):
    """
    Loops over ESGF data sets and scans them for character.

    :param args: (namespace) Namespace object built from attributes parsed from command line
    """
    # Keep track of failures
    count = 0
    failure_count = 0

    # Filter arguments to get a set of file paths to DSIDs
    ds_paths = _get_dataset_paths(args)

    for in args.var_id:
        scanner = scan_dataset(model, experiment, ensemble, var_id)
        count += 1
        if scanner is False:
            failure_count += 1
            continue
        else:
            continue

    percentage_failed = (failure_count / count) * 100

    print(
        f"Completed job. Failure count = {failure_count}. Percentage failed = {percentage_failed}%"
    )


def scan_dataset(project, ds_ids=None, paths=None, facets=None, exclude=None):
    """
    Scans a set of files found for a given `project` based on a combination of:
     - ds_ids: sequence of dataset identifiers (DSIDs)
     - paths: sequence of file paths to scan for NetCDF files under
     - facets: dictionary of facet values to limit the search
     - exclude: list of regular expressions to exclude in file paths

    The scanned datasets are characterised and the output is written to a JSON file
    if no errors occurred.

    Keeps track of whether the job was successful or not.
    Produces error files if an error occurs, otherwise produces a success file.

    :param project: top-level project, e.g. "cmip5", "cmip6" or "cordex" (case-insensitive)
    :param ds_ids: sequence of dataset identifiers (DSIDs), OR None.
    :param paths: sequence of file paths to scan for NetCDF files under, OR None.
    :param facets: dictionary of facet values to limit the search, OR None.
    :param exclude: list of regular expressions to exclude in file paths, OR None.
    :return: Dictionary of {"success": list of DSIDs that were successfully scanned,
                            "failed": list of DSIDs that failed to scan}
    """

    if project not in options.known_projects:
        raise Exception(f'Project must be one of known projects: {options.known_projects}')
    # Generate output file path
    output_path = SETTINGS.JSON_OUTPUT_PATH.format(
        model=model,
        ensemble=ensemble,
        experiment=experiment,
    )

    # create directories to log errors, failures and successes
    open_error_path = SETTINGS.OUTPUT_ERROR_PATH.format(
        model=model,
        ensemble=ensemble,
        experiment=experiment,
    )
    success_path = SETTINGS.SUCCESS_PATH.format(
        model=model,
        ensemble=ensemble,
        experiment=experiment,
    )
    no_files_path = SETTINGS.NO_FILES_PATH.format(
        model=model,
        ensemble=ensemble,
        experiment=experiment,
    )
    extract_error_path = SETTINGS.EXTRACT_ERROR_PATH.format(
        model=model,
        ensemble=ensemble,
        experiment=experiment,
    )
    output_error_path = SETTINGS.OUTPUT_ERROR_PATH.format(
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

    # delete previous failure files and log files
    no_files_file = f"{no_files_path}/{var_id}.log"
    extract_error_file = f"{extract_error_path}/{var_id}.log"
    output_error_file = f"{output_error_path}/{var_id}.log"

    for log_path in (no_files_file, extract_error_file, output_error_file):
        if os.path.exists(log_path):
            os.unlink(log_path)

    # get files
    nc_files = glob.glob(f'ds_id)

    if not nc_files:

        # Log failure: no NC files
        if not os.path.exists(no_files_path):
            os.makedirs(no_files_path)

        open(os.path.join(no_files_path, f"{var_id}.log"), "w")
        return False

    # Open files with Xarray and get character
    ds = xr.open_mfdataset(nc_files)
    character = extract_character(dsid, extract_error_path)

    # Create error file if can't open dataset
    if not ds or not character:

        # Log failure: Could not get character from Xarray Dataset
        if not os.path.exists(open_error_path):
            os.makedirs(open_error_path)

        open(os.path.join(open_error_path, f"{var_id}.log"), "w")
        return False

    # Output to JSON file
    json_file_name = (
        f"cmip5.output1.{model.replace('/', '.')}.{experiment}.mon.land."
        f"Lmon.{ensemble}.latest.{var_id}.json"
    )

    output = to_json(character, output_path, json_file_name, output_error_path, var_id)

    # create error file if can't output file
    if not output:
        return False

    # create success file
    if not os.path.exists(success_path):
        os.makedirs(success_path)

    open(os.path.join(success_path, f"{var_id}.log"), "w")


def main():
    """
    Runs script if called on command line
    """
    args = arg_parse()
    scan_datasets(args)


if __name__ == "__main__":

    main()
