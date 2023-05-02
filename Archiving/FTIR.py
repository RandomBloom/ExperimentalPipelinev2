from collections import Counter
import joblib
import pandas as pd
from archiving_tools import species_code_to_name, nutrient_types
import re
import json

old_lab_root = 'C:/Users/xavie/OneDrive - Brilliant Planet Limited (1)/Files/01. Science Division/04. Cross Department/Labteam Shared PC Files'
labteam_root_data_dir = 'C:/Users/XaviervanGorp/Brilliant Planet Limited/Shared Drive - HQ - Files/01. Science Division/04. Cross Department/Labteam Shared PC Files'
old_root = 'C:/Users/xavie/OneDrive - Brilliant Planet Limited (1)/Files/01. Science Division/01. Primary Production Dept/01. Data Collection/Data'
root_data_dir = 'C:/Users/XaviervanGorp/Brilliant Planet Limited/Shared Drive - HQ - Files/01. Science Division/01. Primary Production Dept/01. Data Collection/01. Primary Productivity'

archiving_folder = 'C:/Users/XaviervanGorp/Brilliant Planet Limited/Shared Drive - HQ - Files/01. Science Division/01. Primary Production Dept/02. Data Analysis/DB_Archiving'

all_csv_summary = joblib.load("C:/Users/XaviervanGorp/OneDrive - SuSeWi Ltd/Desktop/PythonProjects/Susewi/Experimental_pipeline/Data-Backup/FTIR/all_csv_summary.pkl")

save_names = []
good_files = []
es_list = []
for idx, row in all_csv_summary.iterrows():
    fname = row['File name']
    fname = fname.lower().replace('.csv', '')
    if len(fname.split('_')) >= 2:
        num = int(fname.split('_')[1])
    else:
        print(fname)
        good_files.append('Bad file')
        save_names.append('Bad file')
        es_list.append('Bad file')
        continue
    experiment, specie, treatment, rep = row['Experiment'], row['Species'], row['Treatment'], row['Rep']

    file = row['Shared Drive']
    file = str(file).replace(old_root, root_data_dir)

    if str(file) == 'nan':
        file = row['AGRI_SATT folder']
        file = str(file).replace(old_lab_root, labteam_root_data_dir)
    if str(file) == 'nan':
        file = row['Labteam folder']
        file = str(file).replace(old_lab_root, labteam_root_data_dir)

    ES = 'No_info'
    if 'empty' in file.replace(file.split('/')[-1], '').lower():
        ES = 'Empty'
        baseline = 1
    elif 'sample' in file.replace(file.split('/')[-1], '').lower():
        ES = 'Sample'
        baseline = 0
    if ES == 'No_info':
        print(file)
        baseline = None
    es_list.append(baseline)
    experiment, specie, treatment, rep = row['Experiment'], row['Species'], row['Treatment'], row['Rep']
    save_names.append(f"{experiment}_{specie}_{treatment}_{rep}_{ES}_{fname.split('_')[1]}")
    good_files.append(file)

all_csv_summary['Archiving names'] = save_names
all_csv_summary['File'] = good_files
all_csv_summary['Baseline'] = es_list

all_csv_duplicates = all_csv_summary.loc[all_csv_summary.duplicated(subset='Archiving names', keep=False)]
duplicated_SETR_Well = Counter(all_csv_duplicates['Archiving names'])
all_csv_duplicate_filenames = all_csv_summary.loc[all_csv_summary.duplicated(subset='File name', keep=False)]
duplicated_filenames = Counter(all_csv_duplicate_filenames['File name'])


for idx, row in all_csv_summary.iterrows():
    metadata = {}
    file = row['File']
    if 'old' in str(file).lower():
        continue
    if file == 'Bad file':
        continue

    file_source = f"01. Science Division/{file.split('01. Science Division/')[1]}"
    metadata['Archive source'] = file_source
    fname = row['File name']
    metadata['Measurement date'] = f"{fname[:4]}-{fname[4:6]}-{fname[6:8]}"
    well = fname.split('_')[1]
    metadata['Well number'] = well
    metadata['Baseline'] = row['Baseline']
    save_name = row['Archiving names']
    data_fpath = f"{archiving_folder}/FTIR/{save_name}.parquet"
    metadata_fpath = f"{archiving_folder}/FTIR/{save_name}_metadata.json"

    df = pd.read_csv(file, names=['Wavelengths', 'Value'])
    df_data = df.values
    data = df_data.T[1]
    experiment, specie, treatment, rep = row['Experiment'], row['Species'], row['Treatment'], row['Rep']

    metadata['Experiment'] = experiment
    metadata['Species code'] = specie
    metadata['Species name'] = species_code_to_name[specie]
    metadata['Biological replicate'] = int(rep)

    if metadata['Experiment'] == 'Nutrients':
        nutrient = nutrient_types[treatment.split(' ')[0]]
        metadata[nutrient] = float(''.join(re.findall(r'[0-9.]', treatment)))
    else:
        metadata[experiment] = float(''.join(re.findall(r'[0-9.]', treatment.replace('umol m2 s-1', ''))))

    if len(data) == 3734:
        None
    elif len(data) == 3736:
        data = data[1:-1]
    else:
        print('Data wrong length', file)
        continue

    if file in duplicated_filenames.keys() and file in duplicated_SETR_Well:
        data_fpath = f"{archiving_folder}/FTIR/{fname}.parquet"
        metadata['Error messages'] = ['Multiple files for specific species, experiement, treatment, replicate and well',
                                      'More than one file with same name']
        metadata['Error status'] = 1

    elif file in duplicated_filenames.keys():
        print("can't properly id file, duplicated file name")
        print(file)
        metadata['Error messages'] = ['More than one file with same name']
        metadata['Error status'] = 1

    elif file in duplicated_SETR_Well:
        print("can't properly id file, duplicated file name")
        data_fpath = f"{archiving_folder}/FTIR/{fname}.parquet"
        metadata['Error messages'] = ['Multiple files for specific species, experiement, treatment, replicate and well']
        metadata['Error status'] = 1

    df.to_parquet(data_fpath)

    with open(metadata_fpath, "w") as fp:
        metadata['Measurement'] = 'FTIR'
        json.dump(metadata, fp)
