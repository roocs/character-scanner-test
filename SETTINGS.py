import os
join = os.path.join

QUEUE = "short-serial"

WALLCLOCK = "00:30"

# Output path templates
_base_path = './outputs'
LOTUS_OUTPUT_PATH = join(_base_path, 'lotus-outputs', '{ds_ids}')
JSON_OUTPUT_PATH = join(_base_path, 'json-outputs', '{ds_ids}')

SUCCESS_PATH = join(_base_path, 'success', '{ds_ids}')
NO_FILES_PATH = join(_base_path, 'failure', 'no_files/{ds_ids}')
EXTRACT_ERROR_PATH = join(_base_path, 'failure', 'extract_error/{ds_ids}')
OUTPUT_ERROR_PATH = join(_base_path, 'failure', 'output_error/{ds_ids}')

