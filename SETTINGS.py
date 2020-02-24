# lotus settings

QUEUE = "short-serial"

WALLCLOCK = "00:10"

# Output path templates

LOTUS_OUTPUT_PATH = (
    "/home/users/esmith88/roocs/outputs/ALL_OUTPUTS/cmip5/output1/{model}/{experiment}/LOTUS_outputs"
)

JSON_OUTPUT_PATH = "/home/users/esmith88/roocs/outputs/ALL_OUTPUTS/cmip5/output1/{model}/{experiment}/JSON_outputs/{ensemble}"

# ERROR_LOG_PATH = "{current_directory}/ALL_OUTPUTS/cmip5/output1/{model}/{experiment}/error_logs/{ensemble}"

SUCCESS_PATH = "/home/users/esmith88/roocs/outputs/ALL_OUTPUTS/cmip5/output1/{model}/{experiment}/success_files/{ensemble}"

NO_FILES_PATH = "/home/users/esmith88/roocs/outputs/ALL_OUTPUTS/cmip5/output1/{model}/{experiment}/failure_files/no_files/{ensemble}"

OPEN_ERROR_PATH = "/home/users/esmith88/roocs/outputs/ALL_OUTPUTS/cmip5/output1/{model}/{experiment}/failure_files/extract_error/{ensemble}"

EXTRACT_ERROR_PATH = "/home/users/esmith88/roocs/outputs/ALL_OUTPUTS/cmip5/output1/{model}/{experiment}/failure_files/extract_error/{ensemble}"

OUTPUT_ERROR_PATH = "/home/users/esmith88/roocs/outputs/ALL_OUTPUTS/cmip5/output1/{model}/{experiment}/failure_files/output_error/{ensemble}"
