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

import SETTINGS
from lib import options
from lib.character import extract_character


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


def _to_list(item):
    if not item: return item
    return item[0].split(',')


def _to_dict(item):
    if not item: return item
    return dict([_.split('=') for _ in item[0].split(',')])


def parse_args():
    parser = _get_arg_parser()
    args = parser.parse_args()

    project = args.project[0]
    ds_ids = _to_list(args.dataset_ids)
    paths = _to_list(args.paths)
    facets = _to_dict(args.facets)
    exclude = _to_list(args.exclude)

    return project, ds_ids, paths, facets, exclude


def to_json(character, output_path):
    """
    Outputs the extracted characteristics to a JSON file.
    If the characteristics can't be output an error file is produced.

    :param character: (dict) The extracted characteristics.
    :param output_path: (string) The file path at which the JSON file is produced.
    :return : None
    """
    # Output to JSON file
    with open(output_path, 'w') as writer:
        json.dump(character, writer, indent=4, sort_keys=True)


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
            if not dsid: continue

            ds_path = switch_ds(project, dsid) 
            ds_paths[dsid] = ds_path

    # Else use facets if they exist
    elif facets:

        facet_order = options.facet_rules[project]
        facets_as_path = '/'.join([facets.get(_, '*') for _ in facet_order])
     
        pattern = os.path.join(base_dir, facets_as_path)
        print(f'[INFO] Finding dataset paths for pattern: {pattern}')
        
        for ds_path in glob.glob(pattern):
 
            dsid = switch_ds(project, ds_path)
            ds_paths[dsid] = ds_path

    else:
        raise NotImplementedError('Code currently breaks if not using "ds_ids" argument.')

    return ds_paths


def switch_ds(project, ds):
    """
    Switches between ds_path and ds_id.

    :param project: top-level project
    :param ds: either dataset path or dataset ID (DSID)
    :return: either dataset path or dataset ID (DSID) - switched from the input.
    """
    base_dir = options.project_base_dirs[project]

    if ds.startswith('/'):
        return '.'.join(ds.replace(base_dir, '').strip('/').split('/'))
    else:
        return os.path.join(base_dir, '/'.join(ds.split('.')))


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

    print(f'[INFO] Scanning dataset: {ds_id}')
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
        print(f'[ERROR] No data files found for: {ds_path}/*.nc')
        open(outputs['no_files_error'], 'w')
        return False

    # Open files with Xarray and get character
    try:
        character = extract_character(nc_files, var_id=facets['variable'])
    except Exception as exc:
        print(f'[ERROR] Could not load Xarray Dataset for: {ds_path}')
        # Create error file if can't open dataset
        open(outputs['extract_error'], 'w')
        return False

    # Output to JSON file
    try:
        output = to_json(character, outputs['json'])
    except Exception as exc:
        print(f'[ERROR] Could not write JSON output: {outputs["json"]}')
        # Create error file if can't output file
        open(outputs['write_error'], 'w')
        return False

    # Create success file
    open(outputs['success'], 'w')
    print(f'[INFO] Wrote JSON file: {outputs["json"]}')


def main():
    """
    Runs script if called on command line
    """
    project, ds_ids, paths, facets, exclude = parse_args()
    scan_datasets(project, ds_ids, paths, facets, exclude)


if __name__ == "__main__":
    main()
