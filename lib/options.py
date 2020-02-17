models = ['BCC/bcc-csm1-1', 'BCC/bcc-csm1-1-m', 'BNU/BNU-ESM', 'CCCma/CanAM4', 'CCCma/CanCM4',
          'CCCma/CanESM2', 'CMCC/CMCC-CESM', 'CMCC/CMCC-CM', 'CMCC/CMCC-CMS',
          'CNRM-CERFACS/CNRM-CM5', 'CNRM-CERFACS/CNRM-CM5-2', 'COLA-CFS/CFSv2-2011',
          'CSIRO-BOM/ACCESS1-0', 'CSIRO-BOM/ACCESS1-3', 'CSIRO-QCCCE/CSIRO-Mk3-6-0',
          'FIO/FIO-ESM', 'ICHEC/EC-EARTH', 'INM/inmcm4', 'IPSL/IPSL-CM5A-LR', 'IPSL/IPSL-CM5A-MR',
          'IPSL/IPSL-CM5B-LR', 'LASG-CESS/FGOALS-g2', 'LASG-IAP/FGOALS-gl', 'LASG-IAP/FGOALS-s2',
          'MIROC/MIROC-ESM', 'MIROC/MIROC-ESM-CHEM', 'MIROC/MIROC4h', 'MIROC/MIROC5', 'MOHC/HadCM3',
          'MOHC/HadGEM2-A', 'MOHC/HadGEM2-CC', 'MOHC/HadGEM2-ES', 'MPI-M/MPI-ESM-LR',
          'MPI-M/MPI-ESM-MR', 'MPI-M/MPI-ESM-P', 'MRI/MRI-AGCM3-2H', 'MRI/MRI-AGCM3-2S',
          'MRI/MRI-CGCM3', 'MRI/MRI-ESM1', 'NASA-GISS/GISS-E2-H', 'NASA-GISS/GISS-E2-H-CC',
          'NASA-GISS/GISS-E2-R', 'NASA-GISS/GISS-E2-R-CC', 'NASA-GMAO/GEOS-5', 'NCAR/CCSM4',
          'NCC/NorESM1-M', 'NCC/NorESM1-ME', 'NICAM/NICAM-09', 'NIMR-KMA/HadGEM2-AO',
          'NOAA-GFDL/GFDL-CM2p1', 'NOAA-GFDL/GFDL-CM3', 'NOAA-GFDL/GFDL-ESM2G',
          'NOAA-GFDL/GFDL-ESM2M', 'NOAA-GFDL/GFDL-HIRAM-C180', 'NOAA-GFDL/GFDL-HIRAM-C360',
          'NOAA-NCEP/CFSv2-2011', 'NSF-DOE-NCAR/CESM1-BGC', 'NSF-DOE-NCAR/CESM1-CAM5',
          'NSF-DOE-NCAR/CESM1-CAM5-1-FV2', 'NSF-DOE-NCAR/CESM1-FASTCHEM',
          'NSF-DOE-NCAR/CESM1-WACCM']

experiments = ['1pctCO2', 'abrupt4xCO2', 'amip', 'amip4K', 'amip4xCO2', 'amipFuture', 'decadal1960', 'decadal1961',
'decadal1962', 'decadal1963', 'decadal1964', 'decadal1965', 'decadal1966', 'decadal1967', 'decadal1968',
'decadal1969', 'decadal1970', 'decadal1971', 'decadal1972', 'decadal1973', 'decadal1974', 'decadal1975',
'decadal1976', 'decadal1977', 'decadal1978', 'decadal1979', 'decadal1980', 'decadal1981', 'decadal1982',
'decadal1983',
'decadal1984', 'decadal1985', 'decadal1986', 'decadal1987', 'decadal1988', 'decadal1989', 'decadal1990',
'decadal1991', 'decadal1992', 'decadal1993', 'decadal1994', 'decadal1995', 'decadal1996', 'decadal1997',
'decadal1998', 'decadal1999', 'decadal2000', 'decadal2001', 'decadal2002', 'decadal2003', 'decadal2004',
'decadal2005', 'decadal2006', 'esmControl', 'esmFdbk1', 'esmFdbk2', 'esmFixClim1', 'esmFixClim2', 'esmHistorical',
'esmrcp85', 'historical', 'historicalGHG', 'historicalNat', 'midHolocene', 'noVolc1960', 'noVolc1975',
'noVolc1980', 'noVolc1985', 'noVolc1990', 'past1000', 'piControl', 'rcp26', 'rcp45', 'rcp60', 'rcp85',
'sstClim', 'sstClim4xCO2', 'sstClimAerosol', 'sstClimSulfate', 'volcIn2010', 'historicalMisc', 'decadal2007',
'decadal2008', 'decadal2009', 'decadal2010', 'decadal2011', 'historicalExt', 'aqua4K', 'aqua4xCO2',
'aquaControl', 'decadal1959', 'lgm', 'noVolc1965', 'noVolc1970', 'noVolc1995', 'noVolc2000', 'noVolc2005',
'ACCESS1-0', 'ACCESS1-3', 'FGOALS-gl', 'FGOALS-s2', 'MIROC-ESM', 'MIROC-ESM-CHEM', 'MIROC4h',
'MIROC5', 'sst2030', 'decadal2012', 'sst2090', 'sst2090rcp45']


frequency = ['3hr', '6hr', 'day', 'fx', 'mon', 'monClim', 'subhr', 'yr']

realm = ['aerosol', 'atmos', 'land', 'landIce', 'ocean', 'ocnBgchem', 'seaIce']

table_id = ['3hr', '6hrLev', '6hrPlev', 'Amon', 'LImon', 'Lmon', 'OImon', 'Oclim', 'Omon', 'aero', 'cf3hr', 'cfDay',
            'cfMon', 'cfOff', 'cfSites', 'day', 'fx']

ensembles = ['r10i1p1', 'r11i1p1', 'r12i1p1', 'r1i1p1', 'r1i1p121', 'r1i1p122', 'r1i1p124',
             'r1i1p125', 'r1i1p126', 'r1i1p127', 'r1i1p128', 'r1i1p2', 'r1i1p3', 'r1i2p1',
             'r1i2p2', 'r2i1p1', 'r2i1p2', 'r2i1p3', 'r3i1p1', 'r3i1p2', 'r3i1p3', 'r4i1p1',
             'r4i1p2', 'r4i1p3', 'r5i1p1', 'r5i1p2', 'r5i1p3', 'r6i1p1', 'r6i1p2', 'r6i1p3',
             'r7i1p1', 'r8i1p1', 'r9i1p1']

variables = ['baresoilFrac', 'burntArea', 'c3PftFrac', 'c4PftFrac', 'cCwd', 'cLeaf', 'cLitter',
             'cLitterAbove', 'cLitterBelow', 'cMisc', 'cProduct', 'cRoot', 'cSoil', 'cSoilFast',
             'cSoilMedium', 'cSoilSlow', 'cVeg', 'cWood', 'cropFrac', 'evspsblsoi', 'evspsblveg',
             'fFire', 'fGrazing', 'fHarvest', 'fLitterSoil', 'fLuc', 'fVegLitter', 'fVegSoil',
             'gpp', 'grassFrac', 'lai', 'landCoverFrac', 'mrfso', 'mrlsl', 'mrro', 'mrros', 'mrso',
             'mrsos', 'nbp', 'nep', 'npp', 'nppLeaf', 'nppRoot', 'nppWood', 'pastureFrac', 'prveg',
             'rGrowth', 'rMaint', 'ra', 'residualFrac', 'rh', 'shrubFrac', 'tran', 'treeFrac',
             'treeFracPrimDec', 'treeFracPrimEver', 'treeFracSecDec', 'treeFracSecEver', 'tsl']


# models = ['MOHC/HadGEM2-ES']
#
# ensembles = ['r1i1p1']
#
# variables = ['rh']