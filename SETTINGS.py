import os
join = os.path.join

QUEUE = "short-serial"

WALLCLOCK = "00:30"

# Output path templates
_base_path = './outputs'
BASE_LOG_DIR = join(_base_path, 'logs')
BATCH_OUTPUT_PATH = join(BASE_LOG_DIR, 'batch-outputs/{project}/{ds_id}')
JSON_OUTPUT_PATH = join(_base_path, 'register/{project}/{ds_id}.json')

SUCCESS_PATH = join(BASE_LOG_DIR, 'success/{project}/{ds_id}.log')
NO_FILES_PATH = join(BASE_LOG_DIR, 'failure/{project}/no_files/{ds_id}.log')
EXTRACT_ERROR_PATH = join(BASE_LOG_DIR, 'failure/{project}/extract_error/{ds_id}.log')
WRITE_ERROR_PATH = join(BASE_LOG_DIR, 'failure/{project}/write_error/{ds_id}.log')

