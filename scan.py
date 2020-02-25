#!/usr/bin/env python

"""
Takes arguemnts from the command line and scans each dataset to extract the characteristics.
Outputs the characteristics to JSON files.

Can be re-run if errors are fixed and will only run those which failed.
"""

import json
import collections
import os
import glob
import argparse

#import xarray as xr
import string as xr

import SETTINGS
from lib import options


def _get_arg_parser():
    """
    Parses arguments given at the command line

    :return: Namespace object built from attributes parsed from command line.
    """
    parser = argparse.ArgumentParser()
    project_options = options.known_projects

    parser.add_argument(
        "project",
        nargs=1,
        type=str,
        choices=project_options,
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
        "-p",
        "--paths",
        nargs=1,
        type=str,
        default=None,
        required=False,
        help='List of comma-separated directories to search'
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

    return parser


#def _to_list(item):
#    if not item: return item
#    return item.split(',')


def _to_dict(item):
    if not item: return item
    return dict([_.split('=') for _ in item])


def parse_args():
    parser = _get_arg_parser()
    args = parser.parse_args()
    print(args)

    project = args.project[0]
    ds_ids = args.dataset_ids
    paths = args.paths
    facets = _to_dict(args.facets)
    exclude = args.exclude

    return project, ds_ids, paths, facets, exclude


def extract_character(files, var_id):
    """
    Open files as an Xarray MultiFile Dataset and extract character as a dictionary.
    Takes a dataset and extracts characteristics from it.

    :param files: List of data files.
    :param var_id: (string) The variable chosen as an argument at the command line.
    :return character: (dict) The extracted characteristics. Returned as a dictionary.
    """
    # Open the files
    ds = xr.open_mfdataset(files)

    # Get values
    values = ds[var_id].values
    lat_values = ds.lat.values
    lon_values = ds.lon.values
    start_time = ds.time.values[0]
    end_time = ds.time.values[-1]

    # Get info about dataset
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

    return character


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


def get_dataset_paths(project, ds_ids=None, paths=None, facets=None, exclude=None):
    """
    Converts the input arguments into an Ordered Dictionary of {DSID: directory} items.

    :param project: top-level project, e.g. "cmip5", "cmip6" or "cordex" (case-insensitive)
    :param ds_ids: sequence of dataset identifiers (DSIDs), OR None.
    :param paths: sequence of file paths to scan for NetCDF files under, OR None.
    :param facets: dictionary of facet values to limit the search, OR None.
    :param exclude: list of regular expressions to exclude in file paths, OR None.

    :return: An Ordered Dictionary of {dsid: directory}
    """
    base_dir = options.project_base_dirs[project]
    ds_paths = collections.OrderedDict()

    # If ds_ids is defined then ignore all other arguments and use this list
    if ds_ids:

        for dsid in ds_ids:
            ds_path = os.path.join(base_dir, '/'.join(dsid.split('.')))
            ds_paths[dsid] = ds_path
    else:
        raise NotImplementedError('Code currently breaks if not using "ds_ids" argument.')

    return ds_paths


def scan_datasets(project, ds_ids=None, paths=None, facets=None, exclude=None):
    """
    Loops over ESGF data sets and scans them for character.

    Scans multiple ESGF Datasets found for a given `project` based on a combination of:
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
    # Keep track of failures
    count = 0
    failure_count = 0

    # Filter arguments to get a set of file paths to DSIDs
    ds_paths = get_dataset_paths(project, ds_ids=ds_ids, paths=paths, facets=facets, exclude=exclude)

    for ds_id, ds_path in ds_paths.items():
        scanner = scan_dataset(project, ds_id, ds_path)

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


def _get_output_paths(project, ds_id):
    """
    Return a dictionary of output paths to write JSON output, success and failure files to.
    Make each parent directory of not already there.

    :param project: top-level project.
    :param ds_id: Dataset Identifier (DSID)
    :return: dictionary of output paths with keys:
             'success', 'json', 'no_files_error', 'extract_error', 'write_error', 'batch'
    """
    paths = {
        'success': SETTINGS.SUCCESS_PATH.format(**vars()),
        'json': SETTINGS.JSON_OUTPUT_PATH.format(**vars()),
        'no_files_error': SETTINGS.NO_FILES_PATH.format(**vars()),
        'extract_error': SETTINGS.EXTRACT_ERROR_PATH.format(**vars()),
        'write_error': SETTINGS.WRITE_ERROR_PATH.format(**vars()),
        'batch': SETTINGS.BATCH_OUTPUT_PATH.format(**vars())
    }

    # Make directories if not already there
    for pth in paths.values():
        dr = os.path.dirname(pth)

        if not os.path.isdir(dr):
            os.makedirs(dr)

    return paths


def analyse_facets(project, ds_id):
    """

    :param project:
    :param ds_id:
    :return:
    """
    facet_names = options.facet_rules[project]
    facet_values = ds_id.split('.')

    return dict(zip(facet_names, facet_values))


def scan_dataset(project, ds_id, ds_path):
    """
    Scans a set of files found under the `ds_path`.

    The scanned datasets are characterised and the output is written to a JSON file
    if no errors occurred.

    Keeps track of whether the job was successful or not.
    Produces error files if an error occurs, otherwise produces a success file.

    :param project: top-level project, e.g. "cmip5", "cmip6" or "cordex" (case-insensitive)
    :param ds_id: dataset identifier (DSID)
    :param ds_path: directory under which to scan data files.
    :return: Boolean - indicating success of failure of scan.
    """
    if project not in options.known_projects:
        raise Exception(f'Project must be one of known projects: {options.known_projects}')

    facets = analyse_facets(project, ds_id)

    # Generate output file paths
    outputs = _get_output_paths(project, ds_id)

    if os.path.exists(outputs['success']):
        print(f'[INFO] Already ran for: {ds_id}')
        return

    # Delete previous failure files and log files
    for file_key in ('no_files_error', 'extract_error', 'write_error'):

        err_file = outputs[file_key]
        if os.path.exists(err_file):
            os.remove(err_file)

    # Get data files
    nc_files = glob.glob(f'{ds_path}/*.nc')

    if not nc_files:
        # Log failure: no NC files
        open(outputs['no_files_error'], 'w')
        return False

    # Open files with Xarray and get character
    try:
        character = extract_character(nc_files, var_id=facets['variable'])
    except Exception as exc:
        # Create error file if can't open dataset
        open(outputs['extract_error'], 'w')
        return False

    # Output to JSON file
    try:
        output = to_json(character, outputs['json'])
    except Exception as exc:
        # Create error file if can't output file
        open(outputs['write_error'], 'w')
        return False

    # Create success file
    open(outputs['success'], 'w')
    print(f'[INFO] Wrote success file: {outputs["success"]}')


def main():
    """
    Runs script if called on command line
    """
    project, ds_ids, paths, facets, exclude = parse_args()
    scan_datasets(project, ds_ids, paths, facets, exclude)


if __name__ == "__main__":
    main()
