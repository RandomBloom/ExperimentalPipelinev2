import re

species = ['3R6', 'H', 'M38', 'IMS101']
no_si_species = ['H', 'IMS101']
no_nitr_species = ['IMS101']
high_phos_species = ['IMS101']
low_nitr_species = ['M38']

species_names = ['Skeletonema', 'Dunaliella', 'Thalassiosira', 'Trichodesmium']
species_code_to_name = {k: v for k, v in zip(species, species_names)}

nutrient_types = {'N': 'NaNO3', 'P': 'NaH2PO4', 'Si': 'Na2SiO3'}
root_data_dir = 'C:/Users/XaviervanGorp/Brilliant Planet Limited/Shared Drive - HQ - Files/01. Science Division/01. Primary Production Dept/01. Data Collection/01. Primary Productivity'
folder_map = {'Temperature': '01. Temperature', 'Light': '02. Light', 'Nutrients': '03. Nutrients', 'Growth_rates': '01. Growth Rates', 'STAF_Conversions': '02. LabSTAF Conversions', 'Growth_conditions': '03. Growth Conditions', 'Stoichiometry': '04. Stoichiometry', 'Absorption': '05. Light Absorption', 'KPAR': '06. KdPAR', 'FLC': "07. FLC's", 'OLC': "08. OLC's", 'CLC': "09. CLC's", 'FO2': "10. FO2's", 'FTIR': '11. FTIR', 'Nikon': '12. Nikon', 'Combined': 'x. Cross Analysis'}

EXPERIMENT_UNITS = {}
EXPERIMENT_UNITS['Temperature'] = '°C'
EXPERIMENT_UNITS['Light'] = 'μmol m-2 s-1'
EXPERIMENT_UNITS['Nutrients'] = 'μM'

treat_defaults = {'Temperature': 26.0, 'Light': 1120.0, 'NaNO3': 882.0, 'NaH2PO4': 36.0, 'Na2SiO3' : 106.0}

archiving_folder = 'C:/Users/XaviervanGorp/Brilliant Planet Limited/Shared Drive - HQ - Files/01. Science Division/01. Primary Production Dept/02. Data Analysis/DB_Archiving'


def get_file_str_date(fname):
    try:
        date = re.findall(r"\d{6}", fname)[0]
        long_date = re.findall(r"\d{8}", fname)
    except IndexError:
        return 'No date found'

    if not long_date:
        # new_date = f'{date[:2]}/{date[2:4]}/{date[4:]}'
        new_date = f'20{date[4:]}-{date[2:4]}-{date[:2]}'
    elif long_date[0][:3] == '202':
        # new_date = f'{long_date[0][-2:]}/{long_date[0][-4:-2]}/{long_date[0][-6:-4]}'
        new_date = f'{long_date[0][:4]}-{long_date[0][-4:-2]}-{long_date[0][-2:]}'

    else:
        # new_date = f'{long_date[0][:2]}/{long_date[0][2:4]}/{long_date[0][6:]}'
        new_date = f'{long_date[0][4:]}-{long_date[0][2:4]}-{long_date[0][:2]}'

    return new_date


def get_metadata_dict(path):
    metadata = {}
    file_source = f"01. Science Division/{path.split('01. Science Division/')[1]}"
    metadata['Archive source'] = file_source
    metadata['Measurement date'] = get_file_str_date(path.split('/')[-1])
    splitpath = path.split('/')
    ind = None
    for specie in species:
        try:
            ind = splitpath.index(specie)
        except ValueError:
            continue

    if ind is None:
        print(f'No species info found in path {path}')
        return {'path': path}

    metadata['Species code'] = splitpath[ind]
    metadata['Species name'] = species_code_to_name[splitpath[ind]]
    metadata['Experiment'] = splitpath[ind-1].split(' ')[1]

    if 'Old Experiment' in path:
        ind += 1
    metadata['Measurement'] = splitpath[ind+1].split(')')[1].strip()
    if metadata['Experiment'] == 'Nutrients':
        nutrient = splitpath[ind+2].split(' ')[1]
        metadata[nutrient] = float(''.join(re.findall(r'[0-9.]', splitpath[ind+3])))
        metadata['Biological replicate'] = int(path.lower().split('rep')[1].replace('licate', '').strip()[0]) # int(splitpath[ind+4].replace('Rep', ''))
    else:
        metadata['Biological replicate'] = int(path.lower().split('rep')[1].replace('licate', '').strip()[0])
        metadata[metadata['Experiment']] = float(splitpath[ind+2].split('_')[0])
    return metadata


def exp_from_treat(treatment):
    if any([str(i) in treatment for i in [52, 130, 249, 430, 704, 1120]]):
        return 'Light'

    elif any([str(i) in treatment for i in [14, 18, 22, 26, 30, 34, 38]]):
        return 'Temperature'

    else:
        return 'Nutrients'


def treat_str_to_variable_val(treat_str, variable = None):
    if variable is None:
        variable = exp_from_treat(treat_str)
    if 'utrient' in variable:
        for k in nutrient_types.keys():
            if k.lower() in treat_str.lower():
                variable = nutrient_types[k]
    treat_val = float(''.join(re.findall(r'[0-9.]', treat_str)))

    return variable, treat_val


def get_full_treat_info(treat_str, species, experiment = None):
    treat_info = treat_defaults.copy()
    variable, treat_val = treat_str_to_variable_val(treat_str, variable=experiment)
    if species in no_si_species:
        treat_info['Na2SiO3'] = 0
    if species in no_nitr_species:
        treat_info['NaNO3'] = 0
    if species in high_phos_species:
        treat_info['NaH2PO4'] = 43.4
    if (variable in ['NaH2PO4', 'Na2SiO3']) and species == 'M38':
        treat_info['NaNO3'] = 400
    treat_info['Variable'] = variable
    treat_info[variable] = treat_val
    return treat_info


#
# def get_details(path, clean = False):
#     splitpath = path.split('/')
#
#     for specie in species:
#         try:
#             ind = splitpath.index(specie)
#         except ValueError:
#             continue
#
#     specie = splitpath[ind]
#
#     treatment = splitpath[ind+2]
#     rep = splitpath[ind+3]
#
#     experiment = splitpath[ind-1].split(' ')[1]
#
#     if 'Nutrient' in path:
#         treatment_nut = splitpath[ind + 2].split(' ')[1] + ' ' + splitpath[ind + 3]
#         rep_nut = splitpath[ind + 4]
#
#
#         if clean:
#             for k, v in folder_map.items():
#                 specie, treatment_nut, rep_nut, experiment = specie.replace(k, v), treatment_nut.replace(k, v), rep_nut.replace(k, v), experiment.replace(k, v)
#
#         return specie, treatment_nut, rep_nut, experiment
#     else:
#         if clean:
#             for k, v in folder_map.items():
#                 specie, treatment, rep, experiment = specie.replace(k, v), treatment.replace(k, v), rep.replace(k, v), experiment.replace(k, v)
#
#         return specie, treatment, rep, experiment
#
#
# def get_details_disordered(path, include_units=True):
#     print('NEEDS Update for NUTRIENTS')
#     path = path.replace('Light Absorption', 'Absorption')
#
#     exp = 'No experiment found'
#     for experiment in experiments:
#         if experiment in path:
#             exp = experiment
#             break
#
#
#     treatments = TREAT_EXPERIMENT['Temperature'] + TREAT_EXPERIMENT['Light'] + TREAT_EXPERIMENT['Nutrient levels']
#     treatment_types =  TREAT_EXPERIMENT['Nutrient sources'] + TREAT_EXPERIMENT['Nutrient types']
#     clean_split_path = [i for i in path.split('/')]
#     clean_split_path = clean_split_path[:-1] + clean_split_path[-1].split('_')
#
#     splitpath = [i.lower() for i in path.split('/')]
#     splitpath = splitpath[:-1] + splitpath[-1].split('_')
#
#     ind = False
#     for specie in species:
#         try:
#             ind = splitpath.index(specie.lower())
#         except ValueError:
#             continue
#
#     if ind:
#         specie = clean_split_path[ind]
#     else:
#         specie = 'No species found'
#
#     root = 'C:/Users/xavie/OneDrive - Brilliant Planet Limited (1)/Files/01. Science Division'
#     splitpath = path.replace(root, '').replace(')', '.').replace('ep', '.').replace('m2 s-1', '').split('/')
#     splitpath = splitpath[:-1] + splitpath[-1].split('_')
#     splitpath = [''.join(re.findall(r'[0-9.]', i)) for i in splitpath]
#
#     ind = False
#     treat = 'no treatment found'
#     for treat in treatments:
#         try:
#             ind = splitpath.index(str(treat).lower())
#         except ValueError:
#             continue
#         if ind:
#             break
#
#     if exp == 'No experiment found':
#         if treat in temps:
#             exp = 'Temperature'
#         elif treat in pars:
#             exp = 'Light'
#         elif treat in nutrient_treats:
#             exp = 'Nutrients'
#
#
#     if ind:
#         if include_units:
#             treatment = str(treat) + EXPERIMENT_UNITS[exp] # clean_split_path[ind + len(root.split('/')) - 1]
#         else:
#             treatment = str(treat)
#     else:
#         treatment = 'No treatment found'
#
#     splitpath = [i.lower() for i in path.split('/')]
#     splitpath = splitpath[:-1] + splitpath[-1].split('_')
#
#     if 'utrient' in exp:
#         ind = False
#         for treatment_type in treatment_types:
#             try:
#                 ind = splitpath.index(treatment_type.lower())
#             except ValueError:
#                 continue
#
#         if ind:
#             treatment_type = clean_split_path[ind]
#             treatment = f'{treatment_type} {treatment}'
#         else:
#             treatment = 'No level found'
#
#     if 'rep' in path.lower():
#         rep = path.lower().split('rep')[1].replace('licate', '').strip()[0]
#     else:
#         rep = 'No rep info'
#
#     return specie, treatment, rep, exp
