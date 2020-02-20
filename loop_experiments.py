#!/usr/bin/env python

"""
Takes choices from the command line and passes to loop_ensembles.py file for each experiment
"""

import argparse
import subprocess
import os

from lib import options


def arg_parse():
    """
    Parses arguments given at the command line

    :return: Namespace object built from attributes parsed from command line.
    """

    parser = argparse.ArgumentParser()

    model_choices = options.models
    experiment_choices = options.experiments
    ensemble_choices = options.ensembles
    variable_choices = options.variables

    parser.add_argument(
        "-m",
        "--model",
        nargs=1,
        type=str,
        default=model_choices,
        required=True,
        help=f"Institue and model combination to scan, "
        f"must be one of: {model_choices}",
        metavar="",
    )
    parser.add_argument(
        "-exp",
        "--experiment",
        type=str,
        default=experiment_choices,
        help=f"experiment to scan, "
        f"can be one or many of: {experiment_choices}. "
        f"Default is all experiments.",
        metavar="",
        nargs="*",
    )
    parser.add_argument(
        "-e",
        "--ensemble",
        type=str,
        default=ensemble_choices,
        help=f"Ensemble to scan, can be one or many of: "
        f"{ensemble_choices}. Default is all ensembles.",
        metavar="",
        nargs="*",
    )
    parser.add_argument(
        "-v",
        "--var_id",
        choices=variable_choices,
        default=variable_choices,
        help=f"Variable to scan, can be one or many of: "
        f"{variable_choices}. Default is all variables.",
        metavar="",
        nargs="*",
    )
    return parser.parse_args()


def loop_over_experiments(args):
    """
    Runs loop ensembles for each of the experiments listed

    :param args: (namespace) Namespace object built from attributes parsed from command line
    """

    current_directory = os.getcwd()

    ensembles = " ".join(args.ensemble)
    model = " ".join(args.model)
    variables = " ".join(args.var_id)

    # iterate over models
    for experiment in args.experiment:

        # calls loop_ensembles.py from command line
        cmd = (
            f"{current_directory}/loop_ensembles.py -m {model} -exp {experiment} -e "
            f"{ensembles} -v {variables}"
        )
        subprocess.call(cmd, shell=True)


def main():
    """Runs script if called on command line"""

    args = arg_parse()
    loop_over_experiments(args)


if __name__ == "__main__":
    main()
