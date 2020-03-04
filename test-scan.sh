#!/bin/bash

python scan.py -d cmip5.output1.MOHC.HadGEM2-ES.rcp85.mon.atmos.Amon.r1i1p1.latest.tas -m full cmip5

# facets="activity product institute model experiment frequency realm mip_table ensemble_member version variable"
# /badc/cmip5/data/cmip5/output1/*/*/rcp45/mon/ocean/Omon/r1i1p1/latest/zostoga/*

facets="activity=cmip5,product=output1,experiment=rcp45,frequency=mon,realm=ocean,mip_table=Omon,ensemble_member=r1i1p1,version=latest,variable=zostoga"
#python scan.py -f $facets cmip5

#python scan.py -d cmip5.output1.MRI.MRI-CGCM3.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga -m full cmip5

