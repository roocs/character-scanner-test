import json

from scan import scan_datasets
from lib import options


def setup_module(module):
    options.project_base_dirs['c3s-cordex'] = '/group_workspaces/jasmin2/cp4cds1/data'
    module.base_dir = options.project_base_dirs['c3s-cordex']


def test_corrupt_json_file():
    """ Tests what happens when a JSON file exists but is incomplete due to an issue encoding."""
    try:
        ds_id = ["c3s-cordex.output.EUR-11.IPSL.MOHC-HadGEM2-ES.rcp85.r1i1p1.IPSL-WRF381P.v1.day.psl.v20190212"]
        scan_datasets(project='c3s-cordex', ds_ids=ds_id, paths=options.project_base_dirs['c3s-cordex'],
                      mode='quick', location='ceda')
    except json.decoder.JSONDecodeError as exc:
        pass

    # assert os.path.exists(
    #       "./outputs/register/c3s-cordex/output/EUR-11/IPSL/MOHC-HadGEM2-ES/rcp85/r1i1p1/IPSL-WRF381P/v1.day.psl.v20190212.json")


# def test_corrupt_json_file_in_code():
#     """ Tests what happens when a JSON file exists but is incomplete due to an issue encoding."""
#     ds_id = ["c3s-cordex.output.EUR-11.IPSL.MOHC-HadGEM2-ES.rcp85.r1i1p1.IPSL-WRF381P.v1.day.tas.v20190212"]
#     scan_datasets(project='c3s-cordex', ds_ids=ds_id, paths=options.project_base_dirs['c3s-cordex'],
#                   mode='quick', location='ceda')


def teardown_module(module):
    options.project_base_dirs['c3s-cordex'] = '/group_workspaces/jasmin2/cp4cds1/data'
    module.base_dir = options.project_base_dirs['c3s-cordex']