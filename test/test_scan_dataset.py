import json
import pytest

from scan import scan_datasets
from lib import options


def setup_module(module):
    options.project_base_dirs['c3s-cordex'] = '/group_workspaces/jasmin2/cp4cds1/data'
    module.base_dir = options.project_base_dirs['c3s-cordex']


@pytest.mark.skip('This ds id no longer creates a corrupt JSON file')
def test_corrupt_json_file():
    """ Tests what happens when a JSON file exists but is incomplete due to an issue encoding."""
    ds_id = ["c3s-cordex.output.EUR-11.IPSL.MOHC-HadGEM2-ES.rcp85.r1i1p1.IPSL-WRF381P.v1.day.psl.v20190212"]
    scan_datasets(project='c3s-cordex', ds_ids=ds_id, paths=options.project_base_dirs['c3s-cordex'],
                  mode='quick', location='ceda')
    try:
        scan_datasets(project='c3s-cordex', ds_ids=ds_id, paths=options.project_base_dirs['c3s-cordex'],
                      mode='quick', location='ceda')
    except json.decoder.JSONDecodeError as exc:
        pass


def teardown_module(module):
    options.project_base_dirs['c3s-cordex'] = '/group_workspaces/jasmin2/cp4cds1/data'
    module.base_dir = options.project_base_dirs['c3s-cordex']