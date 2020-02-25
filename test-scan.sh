#!/bin/bash

CMIP5_ID1='cmip5.output1.MOHC.HadGEM2-ES.rcp85.mon.atmos.Amon.r1i1p1.latest.tas'

python scan.py -d $CMIP5_ID1 cmip5

#facets="activity product institute model experiment frequency realm mip_table ensemble_member version variable"
# /badc/cmip5/data/cmip5/output1/*/*/rcp45/mon/ocean/Omon/r1i1p1/latest/zostoga/*
facets="activity=cmip5,product=output1,experiment=rcp45,frequency=mon,realm=ocean,mip_table=Omon,ensemble_member=r1i1p1,version=latest,variable=zostoga"

echo $facets
python scan.py -f $facets cmip5

