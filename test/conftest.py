import pytest
from netCDF4 import Dataset
import os

@pytest.fixture
def create_netcdf_file():
    if not os.path.exists("test/data"):
        os.makedirs("test/data")

    if not os.path.exists("test/data/test_file.nc"):
        p = os.path.join("test/data", "test_file.nc")
        test_file = Dataset(p, "w", format="NETCDF4")
        test_file.createDimension("lat", 144)
        test_file.createVariable("lat", "f4", ("lat",))
        test_file.createDimension("lon", 192)
        test_file.createVariable("lon", "f4", ("lon",))

    return "test/data/test_file.nc"
