import subprocess
import os
import pytest

from scan import scan_datasets
from lib import options


def test_c3s_cmip5_base_dir():
    """ Checks definition of c3s cmip5 base dir resolves to a real directory"""
    c3s_cmip5_id = ["c3s-cmip5.output1.MOHC.HadGEM2-ES.rcp85.mon.atmos.Amon.r1i1p1.tas.latest"]
    result = scan_datasets(project='c3s-cmip5', ds_ids=c3s_cmip5_id, paths=options.project_base_dirs['c3s-cmip5'],
                           mode='quick', location='ceda')
    assert os.path.exists("./outputs/register/c3s-cmip5/output1/MOHC/HadGEM2-ES/rcp85/mon/atmos/Amon.r1i1p1.tas.latest.json")


@pytest.mark.skip('FAILS - c3s-cmip6 base dir not defined yet')
def test_c3s_cmip6_base_dir():
    """ Checks definition of c3s cmip6 base dir resolves to a real directory"""
    c3s_cmip6_id = ["c3s-cmip6.CMIP.MOHC.HadGEM3-GC31-LL.amip.r1i1p1f3.Emon.rls.gn.latest"]
    result = scan_datasets(project='c3s-cmip6', ds_ids=c3s_cmip6_id, paths=options.project_base_dirs['c3s-cmip6'],
                           mode='quick', location='ceda')
    assert os.path.exists(
        "./outputs/register/c3s-cmip6/CMIP/MOHC/HadGEM3-GC31-LL/amip/r1i1p1f3/Emon.rls.gn.latest.json")


def test_c3s_cordex_base_dir():
    """ Checks definition of c3s cordex base dir resolves to a real directory"""
    c3s_cordex_id = ["c3s-cordex.output.EUR-11.CNRM.CNRM-CERFACS-CNRM-CM5.rcp45.r1i1p1.CNRM-ALADIN53.v1.day.tas.v20150127"]
    result = scan_datasets(project='c3s-cordex', ds_ids=c3s_cordex_id, paths=options.project_base_dirs['c3s-cordex'],
                           mode='quick', location='ceda')
    assert os.path.exists("./outputs/register/c3s-cordex/output/EUR-11/CNRM/CNRM-CERFACS-CNRM-CM5/rcp45/r1i1p1/CNRM-ALADIN53/v1.day.tas.v20150127.json")

