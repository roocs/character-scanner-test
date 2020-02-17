import os
import subprocess

from lib import options
import SETTINGS


def loop_over_models():
    for model in options.models:
        loop_over_ensembles(model)


def loop_over_ensembles(model):
    for ensemble in options.ensembles:
        loop_over_vars(model, ensemble)


def loop_over_vars(model, ensemble):
    for var_id in options.variables:
        submit_to_lotus(model, ensemble, var_id)


def submit_to_lotus(model, ensemble, var_id):
    # define lotus output file path
    current_directory = os.getcwd()  # get current working directory

    # define lotus output file path
    lotus_output_path = SETTINGS.LOTUS_OUTPUT_PATH_TMPL.format(
        current_directory=current_directory, model=model, ensemble=ensemble)

    # make output directory
    if not os.path.exists(lotus_output_path):
        os.makedirs(lotus_output_path)

    output_base = f"{lotus_output_path}/{var_id}"

    # submit to lotus
    bsub_command = f"bsub -q {SETTINGS.QUEUE} -W {SETTINGS.WALLCLOCK} -o " \
                   f"{output_base}.out -e {output_base}.err {current_directory}" \
                   f"/scanner_test.py -m {model} -e {ensemble} -v {var_id}"
    subprocess.call(bsub_command, shell=True)

    print(f"running {bsub_command}")


def main():
    """Runs script if called on command line"""

    loop_over_models()


if __name__ == '__main__':
    main()
