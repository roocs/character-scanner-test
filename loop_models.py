#!/usr/bin/env python
import argparse
import subprocess
import os

from lib import options


def arg_parse():

    parser = argparse.ArgumentParser()

    model_choices = options.models
    ensemble_choices = options.ensembles
    variable_choices = options.variables

    parser.add_argument('-m', '--model', type=str, default=model_choices,
                        help=f'Institue and model combination to run statistic on, '
                             f'can be one or many of: {model_choices}. '
                             f'Default is all models.', metavar='', nargs='*')
    parser.add_argument('-e', '--ensemble', type=str, default=ensemble_choices,
                        help=f'Ensemble to run statistic on, can be one or many of: '
                             f'{ensemble_choices}. Default is all ensembles.', metavar='',
                        nargs='*')
    parser.add_argument('-v', '--var_id', choices=variable_choices, default=variable_choices,
                        help=f'Variable to run statistic on, can be one or many of: '
                             f'{variable_choices}. Default is all variables.', metavar='',
                        nargs='*')
    return parser.parse_args()


def loop_over_models(args):
    current_directory = os.getcwd()

    ensembles = ' '.join(args.ensemble)
    variables = ' '.join(args.var_id)

    # iterate over models
    for model in args.model:

        # calls loop_ensembles.py from command line
        cmd = f"{current_directory}/loop_ensembles.py -m {model} -e " \
              f"{ensembles} -v {variables}"
        subprocess.call(cmd, shell=True)


def main():
    """Runs script if called on command line"""

    args = arg_parse()
    loop_over_models(args)


if __name__ == '__main__':
    main()
