import os
join = os.path.join

QUEUE = "short-serial"
WALLCLOCK = "00:30"

DIR_GROUPING_LEVEL = 4
CONCERN_THRESHOLD = 0.2

# Output path templates
_base_path = './outputs'
BASE_LOG_DIR = join(_base_path, 'logs')
BATCH_OUTPUT_PATH = join(BASE_LOG_DIR, 'batch-outputs/{grouped_ds_id}')
JSON_OUTPUT_PATH = join(_base_path, 'register/{grouped_ds_id}.json')

SUCCESS_PATH = join(BASE_LOG_DIR, 'success/{grouped_ds_id}.log')
NO_FILES_PATH = join(BASE_LOG_DIR, 'failure/no_files/{grouped_ds_id}.log')
EXTRACT_ERROR_PATH = join(BASE_LOG_DIR, 'failure/extract_error/{grouped_ds_id}.log')
WRITE_ERROR_PATH = join(BASE_LOG_DIR, 'failure/write_error/{grouped_ds_id}.log')

FIX_PATH = join(_base_path, 'fixes/{grouped_ds_id}.json')

