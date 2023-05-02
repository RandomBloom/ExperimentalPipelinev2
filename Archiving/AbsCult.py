import os
import numpy as np
import pandas as pd
from archiving_tools import root_data_dir, get_metadata_dict
import json

archiving_folder = 'C:/Users/XaviervanGorp/Brilliant Planet Limited/Shared Drive - HQ - Files/01. Science Division/01. Primary Production Dept/02. Data Analysis/DB_Archiving'


def get_culture_base_files(filter_date = False, test_run = False):
    files = [os.path.join(root, name)
             for root, dirs, files in os.walk(root_data_dir)
             for name in files
             if name.endswith(".xlsx") and 'Rep' in root and 'Culture' in root]
    if files == []:
        print(f'No files somehow for in vivo')

    files = [file.replace('\\', '/') for file in files]

    if filter_date:
        files = [f for f in files if os.path.getmtime(f) > filter_date]

    if test_run:
        files = files[:test_run]

    return files


def archive_culture_absorption():
    culture_base_files = get_culture_base_files()
    df_cols = ['Wavelength (nm)', 'Tech_rep_1', 'Tech_rep_2', 'Tech_rep_3']
    for file in culture_base_files:
        # noinspection PyTypeChecker
        fname = file.split('/')[-1].split('.')[0]
        data_fpath = f"{archiving_folder}/Absorption_Culture/{fname}.parquet"
        metadata_fpath = f"{archiving_folder}/Absorption_Culture/{fname}_metadata.json"
        try:
            df = pd.read_excel(io=file, engine='openpyxl')
        except Exception as e:
            print(e)
            print(file)
            continue
        raw_file_sources = list(df.columns[1:])
        metadata = get_metadata_dict(file)

        if len(df.columns) == 5:
            df.columns = df_cols + ['Tech_rep_4']
            metadata['Flags'] = ['4 technical reps instead of 3']
            metadata['Raw data source'] = {k:v for k,v in zip(list(df.columns[1:]), raw_file_sources)}
        else:
            try:
                df.columns = df_cols
                metadata['Raw data source'] = {k: v for k, v in zip(list(df.columns[1:]), raw_file_sources)}
            except ValueError:
                metadata['Error status'] = 1
                metadata['Error messages'] = ['Columns mismatch, check file']

        df.to_parquet(data_fpath)

        with open(metadata_fpath, "w") as fp:
            json.dump(metadata, fp)