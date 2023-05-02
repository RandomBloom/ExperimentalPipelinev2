import os
import csv
import pandas as pd
import re
from archiving_tools import exp_from_treat, nutrient_types, species_code_to_name, get_file_str_date, archiving_folder
import json
import numpy as np

rpe_data_folder = 'C:/Users/XaviervanGorp/OneDrive - Brilliant Planet Limited (1)/Desktop/ALL_FLC_calibrated/rpes'


def get_Es_and_idx(data, start=37):
    Es = []
    idx = []
    for i, row in enumerate(data[start:55]):
        # remove all empty strings from row
        row = [elem for elem in row if elem]
        if row != []:
            try:
                Es.append(int(row[0]))
                idx.append(start + i)
            except ValueError:
                raise ValueError('Row {} is not a valid row'.format(i))
        else:
            break

    return Es, idx


for fname in os.listdir(rpe_data_folder):
    file = f'{rpe_data_folder}/{fname}'
    data_fpath = f"{archiving_folder}/FLC/{fname.replace('.csv', '')}.json"
    metadata_fpath = f"{archiving_folder}/FLC/{fname.replace('.csv', '')}_metadata.json"
    data_dict = {}
    metadata = {}
    metadata['Archive source'] = file
    metadata['Measurement date'] = get_file_str_date(fname)

    str_file = fname.lower().replace('rep ', 'rep').replace(' ', '_').replace('_p_', '_p').replace('_si_', '_si').replace('_6_', '_').replace('_5_', '_').replace('_4_', '_').replace('_2_', '_')
    Species = str_file.split('_')[0].upper()
    Treatment = str_file.split('_')[1]
    Experiment = exp_from_treat(Treatment)
    if 'rep' in str_file:
        Replicate = int(str_file.split('rep')[1][0])
        metadata['Biological replicate'] = Replicate
    else:
        metadata['Error messages'] = ['No Replicate info found']
        metadata['Error status'] = 1
    metadata['Species code'] = Species
    metadata['Species name'] = species_code_to_name[Species]
    metadata['Experiment'] = Experiment
    treat_val = float(''.join(re.findall(r'[0-9.]', Treatment)))

    if Experiment == 'Nutrients':
        for k in nutrient_types.keys():
            if k.lower() in Treatment:
                nutrient = nutrient_types[k]
                metadata[nutrient] = treat_val
    else:
        metadata[Experiment] = treat_val
    with open(file) as f:
        reader = csv.reader(f)
        data = [row for row in reader]
    for i, row in enumerate(data[30:38]):
        if 'Up' in row:
            data_index = i + 33

    Es, idx = get_Es_and_idx(data, start=data_index)

    rpe_row = pd.to_numeric([i[3] for i in data[data_index:idx[-1]]])
    if not list(rpe_row[~np.isnan(rpe_row)]):
        metadata['Error messages'] = ['No data found']
        metadata['Error status'] = 1
        with open(metadata_fpath, "w") as fp:
            metadata['Measurement'] = 'FLC'
            json.dump(metadata, fp)
        continue

    data_dict['alpha'] = data[data_index-11][1]
    data_dict['beta'] = data[data_index-10][1]
    data_dict['Ek'] = data[data_index-9][1]
    data_dict['Ekb'] = data[data_index-8][1]
    data_dict['rPM'] = data[data_index-7][1]
    data_dict['Es'] = Es
    data_dict['rP'] = ['0.0'] + [i[3] for i in data[data_index+1:idx[-1]]]
    data_dict['F_u'] = [i[8] for i in data[data_index:idx[-1]]]
    data_dict['Fm_u'] = [i[9] for i in data[data_index:idx[-1]]]
    data_dict['Rho_u'] = [i[19] for i in data[data_index:idx[-1]]]
    data_dict['SigmaPII_u'] = [i[18] for i in data[data_index:idx[-1]]]
    data_dict['TauES_u'] = [i[20] for i in data[data_index:idx[-1]]]
    data_dict['F_d'] = [i[36] for i in data[data_index:idx[-1]]]
    data_dict['Fm_d'] = [i[37] for i in data[data_index:idx[-1]]]
    data_dict['Rho_d'] = [i[47] for i in data[data_index:idx[-1]]]
    data_dict['SigmaPII_d'] = [i[46] for i in data[data_index:idx[-1]]]
    data_dict['TauES_d'] = [i[48] for i in data[data_index:idx[-1]]]

    # data_dict = {k: pd.to_numeric(v, errors='coerce') for k, v in data_dict.items()}

    for k, v in data_dict.items():
        new_v = pd.to_numeric(v, errors='coerce')
        try:
            new_v = float(new_v)
        except TypeError:
            new_v = list(map(float, new_v))
        data_dict[k] = new_v

    with open(data_fpath, "w") as fp:
        json.dump(data_dict, fp)

    with open(metadata_fpath, "w") as fp:
        metadata['Measurement'] = 'FLC'
        json.dump(metadata, fp)

