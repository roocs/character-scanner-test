import os

from lib import options

import SETTINGS


def get_grouped_ds_id(ds_id):

    # Define a "grouped" ds_id that splits facets across directories and then groups
    # the final set into a file path, based on SETTINGS.DIR_GROUPING_LEVEL value
    gl = SETTINGS.DIR_GROUPING_LEVEL
    parts = ds_id.split('.')
    grouped_ds_id = '/'.join(parts[:-gl]) + '/' + '.'.join(parts[-gl:])

    return grouped_ds_id


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

