import os
join = os.path.join

QUEUE = "short-serial"
WALLCLOCK = "00:30"

DIR_GROUPING_LEVEL = 4

# Output path templates
_base_path = './outputs'
BASE_LOG_DIR = join(_base_path, 'logs')
BATCH_OUTPUT_PATH = join(BASE_LOG_DIR, 'batch-outputs/{project}/{grouped_ds_id}')
JSON_OUTPUT_PATH = join(_base_path, 'register/{project}/{grouped_ds_id}.json')

SUCCESS_PATH = join(BASE_LOG_DIR, 'success/{project}/{grouped_ds_id}.log')
NO_FILES_PATH = join(BASE_LOG_DIR, 'failure/{project}/no_files/{grouped_ds_id}.log')
EXTRACT_ERROR_PATH = join(BASE_LOG_DIR, 'failure/{project}/extract_error/{grouped_ds_id}.log')
WRITE_ERROR_PATH = join(BASE_LOG_DIR, 'failure/{project}/write_error/{grouped_ds_id}.log')

