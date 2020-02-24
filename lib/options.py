project_base_dirs = {
    'cmip5': '/badc/cmip5/data',
    'cmip6': '/badc/cmip6/data',
    'cordex': '/badc/cordex/data'
}

known_projects = project_base_dirs.keys()

facet_rules = {
    'cmip5': 'activity product institute model experiment frequency realm mip_table ensemble_member version variable'.split(),
    'cmip6': 'mip_era activity_id institution_id source_id experiment_id member_id table_id variable_id grid_label version'.split(),
    'cordex': 'NOT DEFINED YET'
}

"""
[DEFAULT]
use_esdoc = true
dataset_glob_path = */*/*
collection_glob_path = */*
unknown_party_ob_id = 9
global_geog_bbox_ob_id = 529
uses_latest_symlinks = true
# Override 'project_id_in_paths' if project ID (or section header) is
# different from the directory name found in file paths.
institute_facet = institute
project_id_in_paths =
constraints_ob_id =

[cmip5]
activity = cmip5
base_path = /badc/cmip5/data
m2m_cache_dir = /badc/cmip5/metadata/mip-to-moles/scans
base_dirs = /badc/cmip5/data/cmip5/output1 /badc/cmip5/data/cmip5/output2
dataset_level_glob = /badc/cmip5/data/cmip5/output*/*/*/*
above_version_dir_glob_template = {}/*/*/*/r*
version_dir_glob_templates = {}/v[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9] {}/v[0-9]
nc_file_glob_template = {}/*/*.nc
eg_file = /badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/rcp45/mon/atmos/Amon/r1i1p1/v20111128/tasmax/tasmax_Amon_HadGEM2-ES_rcp45_r1i1p1_200512-203011.nc
facets = activity product institute model experiment frequency realm mip_table ensemble_member version variable
ceda_officers = Charlotte Pascoe
dq_conformance_result_ob_id = 3045

[cmip6]
project_id_in_paths = CMIP6
activity = cmip6
m2m_cache_dir = /badc/cmip6/metadata/mip-to-moles/scans
institute_facet = institution_id
base_path = /badc/cmip6/data/
#/group_workspaces/jasmin4/esgf_fedcheck/cache/data
base_dirs = /badc/cmip6/data/CMIP6/
#/group_workspaces/jasmin4/esgf_fedcheck/cache/data/CMIP6
dataset_level_glob = /badc/cmip6/data/CMIP6/*/*/*/*
#/group_workspaces/jasmin4/esgf_fedcheck/cache/data/CMIP6/*/*/*/*
above_version_dir_glob_template = {}/*/*/*/*
version_dir_glob_templates = {}/v[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]
nc_file_glob_template = {}/*.nc
eg_file = /badc/cmip6/data/CMIP6/HighResMIP/MOHC/HadGEM3-GC31-HH/hist-1950/r1i1p1f1/Amon/tas/gn/v20171213/tas_Amon_HadGEM3-GC31-HH_hist-1950_r1i1p1f1_gn_201001-201012.nc
facets = mip_era activity_id institution_id source_id experiment_id member_id table_id variable_id grid_label version
example_values = mip_era:CMIP6 activity_id:HighResMIP institution_id:MOHC source_id:HadGEM3-GC31-HH experiment_id:hist-1950 member_id:r1i1p1f1 table_id:Amon variable_id:tas grid_label:gn version:v20180418
use_esdoc = false
ceda_officers = Ruth Petrie
dq_conformance_result_ob_id = 1
#3334
constraints_ob_id = 1
#2310


"""
