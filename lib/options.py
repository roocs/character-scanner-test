project_base_dirs = {
    'cmip5': '/badc/cmip5/data',
    'cmip6': '/badc/cmip6/data',
    'cordex': '/badc/cordex/data'
    'c3s-cmip5': '/group_workspaces/jasmin2/cp4cds1/data',
    'c3s-cmip6': 'NOT DEFINED YET',
    'c3s-cordex': '/group_workspaces/jasmin2/cp4cds1/data/c3s-cordex',
}

known_projects = project_base_dirs.keys()

locations = ['ceda', 'dkrz', 'other']

facet_rules = {
    'cmip5': 'activity product institute model experiment frequency realm mip_table ensemble_member version variable'.split(),
    'cmip6': 'mip_era activity_id institution_id source_id experiment_id member_id table_id variable_id grid_label version'.split(),
    'cordex': 'project product domain institute driving_model experiment ensemble rcm_name rcm_version time_frequency variable'.split(),
    'c3s-cmip5': 'activity product institute model experiment frequency realm mip_table ensemble_member variable version'.split(),
    'c3s-cmip6': 'mip_era activity_id institution_id source_id experiment_id member_id table_id variable_id grid_label version'.split(),
    'c3s-cordex': 'project product domain institute driving_model experiment ensemble rcm_name rcm_version time_frequency variable'.split()
}


"""
dataset_id = cordex.%(product)s.%(domain)s.%(institute)s.%(driving_model)s.%(experiment)s.%(ensemble)s.%(rcm_name)s.%(rcm_version)s.%(time_frequency)s.%(variable)s

directory_format = %(root)s/%(project)s/%(product)s/%(domain)s/%(institute)s/%(driving_model)s/%(experiment)s/%(ensemble)s/%(rcm_model)s/%(rcm_version)s/%(time_frequency)s/%(variable)s/%(version)s
"""
