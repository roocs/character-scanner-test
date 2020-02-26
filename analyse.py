import argparse

from SETTINGS import _base_path


def _get_arg_parser():
    parser = argparse.ArgumentParser()
    project_options = options.known_projects

    parser.add_argument(
        "project",
        nargs=1,
        type=str,
        choices=project_options,
        help=f'Project ID, must be one of: {project_options}'
    )

    parser.add_argument(
        "-d",
        "--dataset-ids",
        nargs=1,
        type=str,
        default=None,
        required=True,
        help='List of comma-separated dataset identifiers'
    )

    return parser


def parse_args():
    parser = _get_arg_parser()
    args = parser.parse_args()

    project = args.project[0]
    ds_ids = args.dataset_ids.split(',')

    return project, ds_ids


def analyse_datasets(ds_ids):
    "Compares a set of dataset identifiers"

   sdfds 


def main():
    
    project, ds_ids = parse_args()
    analyse_datasets(ds_ids)


if __name__ == '__main__':

    main()

