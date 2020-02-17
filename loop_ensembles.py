#!/usr/bin/env python
import argparse
import os
#import xarray as xr
import subprocess

from lib import options
import SETTINGS


def arg_parse():
    parser = argparse.ArgumentParser()

    model_choices = options.models
    ensemble_choices = options.ensembles
    variable_choices = options.variables

    parser.add_argument('-m', '--model', nargs=1, type=str, default=model_choices,
                        required=True, help=f'Institue and model combination to run statistic on, '
                                            f'must be one of: {model_choices}', metavar='')
    parser.add_argument('-e', '--ensemble', type=str, default=ensemble_choices,
                        help=f'Ensemble to run statistic on, can be one or many of: '
                             f'{ensemble_choices}. Default is all ensembles.', metavar='',
                        nargs='*')
    parser.add_argument('-v', '--var_id', choices=variable_choices, default=variable_choices,
                        help=f'Variable to run statistic on, can be one or many of: '
                             f'{variable_choices}. Default is all variables', metavar='',
                        nargs='*')
    return parser.parse_args()


def loop_over_ensembles(args):
    # turn arguments into string
    model = ' '.join(args.model)
    variables = ' '.join(args.var_id)

    # iterate over each ensemble
    for ensemble in args.ensemble:

        # define lotus output file path
        current_directory = os.getcwd()  # get current working directory

        # define lotus output file path
        lotus_output_path = SETTINGS.LOTUS_OUTPUT_PATH_TMPL.format(
            current_directory=current_directory, model=model)

        # make output directory
        if not os.path.exists(lotus_output_path):
            os.makedirs(lotus_output_path)

        output_base = f"{lotus_output_path}/{ensemble}"

        # submit to lotus
        bsub_command = f"bsub -q {SETTINGS.QUEUE} -W {SETTINGS.WALLCLOCK} -o " \
                       f"{output_base}.out -e {output_base}.err {current_directory}" \
                       f"/scan.py -m {model} -e {ensemble} -v {variables}"
        subprocess.call(bsub_command, shell=True)

        print(f"running {bsub_command}")


def main():
    """Runs script if called on command line"""

    args = arg_parse()
    loop_over_ensembles(args)


if __name__ == '__main__':
    main()
