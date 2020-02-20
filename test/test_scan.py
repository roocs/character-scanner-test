import xarray as xr
import subprocess
import glob
import sys
import pytest
import os

import scan


def test_parser():
    sys.argv = 'scan.py -m MOHC/HadGEM2-ES -exp historical -e r1i1p1 -v rh'.split()
    args = scan.arg_parse()
    for model in args.model:
        assert model == 'MOHC/HadGEM2-ES'
    for experiment in args.experiment:
        assert experiment == 'historical'
    for ensemble in args.ensemble:
        assert ensemble == 'r1i1p1'
    for variable in args.var_id:
        assert variable == 'rh'


def test_get_files():
    model = 'MOHC/HadGEM2-ES'
    experiment = 'historical'
    ensemble = 'r1i1p1'
    var_id = 'rh'

    nc_files = scan.find_files(model, experiment, ensemble, var_id)
    assert nc_files == ['/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/historical/mon/land/'
                        'Lmon/r1i1p1/latest/rh/rh_Lmon_HadGEM2-ES_historical_r1i1p1_185912-188411.nc',
                        '/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/historical/mon/land/'
                        'Lmon/r1i1p1/latest/rh/rh_Lmon_HadGEM2-ES_historical_r1i1p1_188412-190911.nc',
                        '/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/historical/mon/land/'
                        'Lmon/r1i1p1/latest/rh/rh_Lmon_HadGEM2-ES_historical_r1i1p1_190912-193411.nc',
                        '/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/historical/mon/land/'
                        'Lmon/r1i1p1/latest/rh/rh_Lmon_HadGEM2-ES_historical_r1i1p1_193412-195911.nc',
                        '/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/historical/mon/land/'
                        'Lmon/r1i1p1/latest/rh/rh_Lmon_HadGEM2-ES_historical_r1i1p1_195912-198411.nc',
                        '/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/historical/mon/land/'
                        'Lmon/r1i1p1/latest/rh/rh_Lmon_HadGEM2-ES_historical_r1i1p1_198412-200511.nc']


def test_extract_characteristics_no_error(tmpdir):
    model = 'MOHC/HadGEM2-ES'
    experiment = 'historical'
    ensemble = 'r1i1p1'
    var_id = 'rh'

    nc_files = scan.find_files(model, experiment, ensemble, var_id)
    ds = xr.open_mfdataset(nc_files)
    extract_error_path = tmpdir.mkdir("test_extract_error")

    characteristics = scan.extract_characteristic(ds, extract_error_path, var_id)

    assert len(characteristics) == 26


def test_extract_characteristics_with_error(tmpdir, create_netcdf_file):
    """ Tests correct thing happens when a characteristic can't be extracted"""
    var_id = 'fake'

    ds = xr.open_dataset(create_netcdf_file)
    extract_error_path = tmpdir.mkdir("test_extract_error")

    characteristics = scan.extract_characteristic(ds, extract_error_path, var_id)

    assert characteristics == False


def test_output_to_JSON(tmpdir, create_netcdf_file):
    var_id = 'fake'

    ds = xr.open_dataset(create_netcdf_file)
    characteristics = {'dims': ds.dims} #dims isn't serializable so should return False
    output_path = tmpdir.mkdir("test_output")
    output_error_path = tmpdir.mkdir("test_output_error")
    json_file_name = 'json_test.json'

    JSON = scan.output_to_JSON(characteristics, output_path, json_file_name, output_error_path, var_id)

    assert JSON == False
     

def test_already_run_output():
    # check nothing returned if success file already produced
    fpath = 'ALL_OUTPUTS/cmip5/output1/MOHC/HadGEM2-ES/historical/JSON_outputs/r1i1p1/cmip5.output1.MOHC.HadGEM2-ES.historical.mon.land.Lmon.r1i1p1.latest.rh.json'
    if os.path.exists(fpath):
        os.unlink(fpath)
    cmd = 'python scan.py -m MOHC/HadGEM2-ES -exp historical -e r1i1p1 -v rh'
    subprocess.call(cmd, shell=True)
    scanner = scan.scan('MOHC/HadGEM2-ES', 'historical', 'r1i1p1', 'rh')
    assert scanner is None

    cmd_delete = 'rm -r ALL_OUTPUTS/cmip5/output1/MOHC/HadGEM2-ES/historical/JSON_outputs/r1i1p1/cmip5.output1.' \
                 'MOHC.HadGEM2-ES.historical.mon.land.Lmon.r1i1p1.latest.rh.json ' \
                 'ALL_OUTPUTS/cmip5/output1/MOHC/HadGEM2-ES/historical/success_files/r1i1p1/rh.log'
    subprocess.call(cmd_delete, shell=True)


def test_scan_no_files():
    # no files for this file path
    scanner = scan.scan('MOHC/HadGEM2-ES', 'historical', 'r1i1p1', 'cMisc')
    assert scanner == False

# def test_loop_over_vars():
#
# def test_scan_extract_error(): # need example of a file that has a characteristic that can't be extracted
#
# def test_scan_output_error(): # need example of a file that has a characteristic that can't be dumped to json file
#
# def test_scan_open_error(): # need example of a file set that can't be opened using mfdataset