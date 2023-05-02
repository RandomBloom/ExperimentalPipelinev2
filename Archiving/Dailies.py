import joblib
import pandas as pd
from collections import Counter
import numpy as np
from archiving_tools import species_code_to_name
import datetime
import json

previous_root_data_dir = 'C:/Users/XaviervanGorp/Brilliant Planet Limited/Shared Drive - HQ - Files/01. Science Division/01. Primary Production Dept/01. Data Collection/Data'
root_data_dir = 'C:/Users/XaviervanGorp/Brilliant Planet Limited/Shared Drive - HQ - Files/01. Science Division/01. Primary Production Dept/01. Data Collection/01. Primary Productivity'
archiving_folder = 'C:/Users/XaviervanGorp/Brilliant Planet Limited/Shared Drive - HQ - Files/01. Science Division/01. Primary Production Dept/02. Data Analysis/DB_Archiving'


def archive_daily_measures_data():
    paths = joblib.load('Dailies_paths.pkl')

    dfs_saved = []
    paths = [path.replace(previous_root_data_dir, root_data_dir) for path in paths]

    for path in paths:

        print(path)
        split_path = path.split('/')

        split_path[6] = split_path[6].replace('%20', ' ')
        sheets = pd.ExcelFile(path).sheet_names

        skip_sheets = ['Conditions', 'Coefficients', 'Summary (Counts)', 'Summary (STAF)', 'Cells vs Fo', 'Growth rates']

        for sheet in sheets:
            if sheet in skip_sheets:
                continue
            if sheet == '3' and 'M38' in path and 'Temperature' in path:
                continue

            metadata = {}
            file_source = f"01. Science Division/{path.split('01. Science Division')[1]}"
            metadata['Archive source'] = file_source
            metadata['Sheet name'] = sheet

            experiment = split_path[9].split(' ')[1]
            species = split_path[10]
            data_fpath = f'{archiving_folder}/Dailies/{experiment}_{species}_{sheet}.parquet'
            metadata_fpath = f'{archiving_folder}/Dailies/{experiment}_{species}_{sheet}_metadata.json'

            metadata['Experiment'] = experiment
            metadata['Species code'] = species
            metadata['Species name'] = species_code_to_name[species]
            metadata['Sheet source'] = sheet

            df = pd.read_excel(io=path, sheet_name=sheet, engine='openpyxl')

            columns = list(df.columns)
            first_row = list(df.iloc[0].fillna(''))
            df_columns = []
            for i, row in enumerate(first_row):
                if row == '' or row in ['Independent', 'NaNO3', 'Na2SiO3 · 5H2O', 'NaH2PO4']:
                    df_columns.append(columns[i])
                else:
                    df_columns.append(row)

            counts = Counter(list(df_columns))

            df_columns_unique = []
            for i, row in enumerate(df_columns):
                if counts[row] > 1:
                    df_columns_unique.append(columns[i] + ' ' + row)
                else:
                    df_columns_unique.append(row)

            if 'Nutrient' in path:
                for i in first_row[:3]:
                    if i == 'Independent':
                        continue
                    else:
                        variable = i.replace(' · 5H2O', '')
            else:
                variable = experiment

            df.columns = df_columns_unique
            df.drop(0, inplace=True)
            df.dropna(axis=0, how='all', inplace=True)

            df['Incubator'] = [sheet] * len(df.index)
            df['Species'] = [species] * len(df.index)
            df['Experiment'] = [experiment] * len(df.index)
            df['Variable'] = [variable] * len(df.index)

            comm_col = [col for col in df.columns if 'Comment' in col]

            comms = []
            for idx, row in df.iterrows():
                comm_list = list(row[comm_col].dropna().values)
                comm_list = [str(i) for i in comm_list if i != '']
                comment = '/'.join(comm_list).strip(',')
                comment = comment.replace('/', ' / ')
                comms.append(comment)

            df['Comments'] = comms

            df = get_dailies_reduced_cols(path, df)

            df.columns, fill_cols = get_dailies_cols_final(path)

            values = {}
            for fill_col in fill_cols:
                values[fill_col] = np.mean(pd.to_numeric(df[fill_col].dropna(), errors='coerce'))
            df.fillna(value=values, inplace=True)

            # if 'Nutrient' in path:
            #     treat_info = [i for i in first_row[:3] if i != 'Independent'][0].replace(' · 5H2O', '')
            # else:
            #     treat_info = str(int(df.iloc[0, 0]))

            df['Date (dd/mm/yy)'] = pd.to_datetime(df['Date (dd/mm/yy)'], errors='coerce')

            df = df[df['Date (dd/mm/yy)'] < pd.to_datetime(datetime.datetime.now())]

            df['Time (hh:mm:ss)'] = [i if (type(i) == datetime.time) else np.nan for i in df['Time (hh:mm:ss)']]

            for col in df.columns:
                if col in ['Experiment', 'Species', 'Incubator', 'Variable', 'Date (dd/mm/yy)', 'Time (hh:mm:ss)', 'Magnification', 'Comments']:
                    continue
                else:
                    df[col] = pd.to_numeric(df[col], errors='coerce')

            if data_fpath in dfs_saved:
                print('appending to', data_fpath.split('/')[-1])
                old_df = pd.read_parquet(data_fpath)
                new_df = pd.concat([old_df, df])
                new_df.to_parquet(data_fpath)
            else:
                df.to_parquet(data_fpath)
                dfs_saved.append(data_fpath)

            with open(metadata_fpath, "w") as fp:
                metadata['Measurement'] = 'Dailies'
                json.dump(metadata, fp)


def get_dailies_reduced_cols(path, df):

    if 'Temperature' in path and 'M38' in path:
        return df[['Experiment', 'Variable', 'Species', 'Temperature (°C)', 'Incubator', 'Date (dd/mm/yy)', 'Time (hh:mm:ss)', 'Experimental Day',
                'Hours (Between Sampling)', 'Hours (Culturing Time)', 'Nikon Ti2 n Cells (Pre-Dilution)',
                'Pipette Volume (µl)', 'Magnification', 'Mean Cell Width (µm)', 'Mean Cell Length (µm)',
                'Unnamed: 18 Cells/mL', 'Unnamed: 19 Ln Cells', 'Unnamed: 20 µ (d-1)', 'Unnamed: 21 Generations',
                'NSV', 'NPQ', 'ρ', 'σPII', 'αPII', 'τF', 'dρ', 'dσPII', 'dαPII', 'τS', 'Unnamed: 33 Fo',
                'Unnamed: 34 Fm', 'Fv', 'Fv/Fm', 'Unnamed: 42 µ (d-1)',
                'Unnamed: 43 Generations', '(Free)', '°C', '(mg/L)', 'µatm', 'HCO3- µmol/kg ASW', 'CO32- µmol/kg ASW',
                'CO2 µmol/kg ASW', 'TCO2 µmol/kg ASW', 'g', 'µg', 'Gross P-consumed µM', 'P concentration µM',
                'Unnamed: 65 µmol kg ASW', 'Unnamed: 68 µmol kg ASW', 'Dilution Rate (%)', 'Target Culture Volume (mL)',
                'Culture Before Dilution (mL)', '1) Media to Add (mL)', '2) Culture Discard (mL)',
                '3) Remaining Culture (mL)', '4) Media to Add (mL)', 'Culture After Dilution (mL)',
                'Nikon Cell Density After Dilution (/mL)', 'Fo after Dilution', 'Comments']]

    if 'Temperature' in path:
        try:
            return df[['Experiment', 'Variable', 'Species', 'Temperature (°C)', 'Incubator', 'Date (dd/mm/yy)', 'Time (hh:mm:ss)', 'Experimental Day',
             'Hours (Between Sampling)',
             'Hours (Culturing Time)', 'Nikon Ti2 n Cells (Pre-Dilution)', 'Pipette Volume (µl)', 'Magnification',
             'Mean Cell Width (µm)', 'Mean Cell Length (µm)', 'Unnamed: 18 Cells/mL', 'Unnamed: 19 Ln Cells',
             'Unnamed: 20 µ (d-1)', 'Unnamed: 21 Generations', 'NSV', 'NPQ', 'ρ', 'σPII', 'αPII', 'τF', 'dρ',
             'dσPII', 'dαPII', 'τS', 'Unnamed: 37 Fo', 'Unnamed: 38 Fm', 'Fv', 'Fv/Fm', 'Unnamed: 41 µ (d-1)',
             'Unnamed: 42 Generations', '(Free)', '°C', '(mg/L)', 'µatm', 'HCO3- µmol/kg ASW', 'CO32- µmol/kg ASW',
             'CO2 µmol/kg ASW', 'TCO2 µmol/kg ASW', 'g', 'µg', 'Gross P-consumed µM', 'P concentration µM',
             'Unnamed: 64 µmol kg ASW', 'Unnamed: 67 µmol kg ASW',
             'Dilution Rate (%)', 'Target Culture Volume (mL)', 'Culture Before Dilution (mL)',
             '1) Media to Add (mL)',
             '2) Culture Discard (mL)', '3) Remaining Culture (mL)', '4) Media to Add (mL)',
             'Culture After Dilution (mL)',
             'Nikon Cell Density After Dilution (/mL)', 'Fo after Dilution', 'Comments']]
        except KeyError:
            return df[['Experiment', 'Variable', 'Species', 'Temperature (°C)', 'Incubator', 'Date (dd/mm/yy)', 'Time (hh:mm:ss)',
                    'Experimental Day', 'Hours (Between Sampling)',
                    'Hours (Culturing Time)',
                    'Nikon Ti2 n Cells (Pre-Dilution)', 'Pipette Volume (µl)',
                    'Magnification', 'Mean Cell Width (µm)', 'Mean Cell Length (µm)',
                    'Unnamed: 18 Cells/mL', 'Unnamed: 19 Ln Cells', 'Unnamed: 20 µ (d-1)',
                    'Unnamed: 21 Generations', 'NSV', 'NPQ', 'ρ', 'σPII', 'αPII', 'τF', 'dρ',
                    'dσPII', 'dαPII', 'τS', 'Unnamed: 37 Fo', 'Unnamed: 38 Fm',
                    'Fv', 'Fv/Fm', 'Unnamed: 46 µ (d-1)', 'Unnamed: 47 Generations', 'Unnamed: 51 Generations',
                    '(Free)', '°C', '(mg/L)',
                    'µatm', 'HCO3- µmol/kg ASW', 'CO32- µmol/kg ASW', 'CO2 µmol/kg ASW',
                    'TCO2 µmol/kg ASW', 'g', 'µg', 'Gross P-consumed µM',
                    'P concentration µM', 'Unnamed: 69 µmol kg ASW', 'Dilution Rate (%)',
                    'Target Culture Volume (mL)', 'Culture Before Dilution (mL)',
                    '1) Media to Add (mL)', '2) Culture Discard (mL)',
                    '3) Remaining Culture (mL)', '4) Media to Add (mL)',
                    'Culture After Dilution (mL)',
                    'Nikon Cell Density After Dilution (/mL)', 'Fo after Dilution', 'Comments']]




    elif 'Light' in path:
        return df[['Experiment', 'Variable', 'Species', 'Light (uE)', 'Incubator', 'Date (dd/mm/yy)', 'Time (hh:mm:ss)', 'Experimental Day',
         'Hours (Between Sampling)',
         'Hours (Culturing Time)', 'Nikon Ti2 n Cells (Pre-Dilution)', 'Pipette Volume (µl)', 'Magnification',
         'Mean Cell Width (µm)', 'Mean Cell Length (µm)', 'Unnamed: 18 Cells/mL', 'Unnamed: 19 Ln Cells',
         'Unnamed: 20 µ (d-1)', 'Unnamed: 21 Generations', 'NSV', 'NPQ', 'ρ', 'σPII', 'αPII', 'τF',
         'dρ', 'dσPII', 'dαPII', 'τS', 'Unnamed: 37 Fo', 'Unnamed: 38 Fm', 'Fv', 'Fv/Fm', 'Unnamed: 41 µ (d-1)',
         'Unnamed: 42 Generations', '(Free)', '°C', '(mg/L)', 'µatm', 'HCO3- µmol/kg ASW', 'CO32- µmol/kg ASW',
         'CO2 µmol/kg ASW', 'TCO2 µmol/kg ASW', 'g', 'µg', 'Gross P-consumed µM', 'P concentration µM',
         'Unnamed: 64 µmol kg ASW', 'Unnamed: 67 µmol kg ASW',
         'Dilution Rate (%)', 'Target Culture Volume (mL)', 'Culture Before Dilution (mL)',
         '1) Media to Add (mL)',
         '2) Culture Discard (mL)', '3) Remaining Culture (mL)', '4) Media to Add (mL)',
         'Culture After Dilution (mL)',
         'Nikon Cell Density After Dilution (/mL)', 'Fo after Dilution', 'Comments']]

    elif 'Nutrient' in path and 'IMS101' in path:
        return df[['Experiment', 'Variable', 'Species', 'Target N (µM)', 'Target P (µM)', 'Target Si (µM)', 'Incubator', 'Date (dd/mm/yy)',
     'Time (hh:mm:ss)', 'Experimental Day', 'Hours (Between Sampling)',
     'Hours (Culturing Time)', 'n Cells (Pre-Dilution)',
     'Unnamed: 9 Pipette Volume (µl)', 'Unnamed: 10 Magnification',
     'Unnamed: 11 Mean Cell Width (µm)', 'Unnamed: 12 Mean Cell Length (µm)',
     'Cells/mL', 'Ln Cells', 'Unnamed: 15 µ (d-1)',
     'Unnamed: 16 Generations', '∑EPI (Pre-Dilution)',
     'Unnamed: 19 Pipette Volume (µl)', 'Unnamed: 20 Magnification',
     'Unnamed: 21 Mean Cell Width (µm)', 'Unnamed: 22 Mean Cell Length (µm)',
     '∑EPI/mL', 'Ln EPI', 'Unnamed: 25 µ (d-1)', 'Unnamed: 26 Generations',
     'NSV', 'NPQ', 'ρ', 'σPII', 'αPII', 'τF', 'dρ',
     'dσPII', 'dαPII', 'τS', 'Unnamed: 38 Fo', 'Unnamed: 39 Fm',
     'Fv', 'Fv/Fm',
     'Unnamed: 47 µ (d-1)', 'Unnamed: 48 Generations', '(Free)', '°C', '(mg/L)',
     'µatm', 'HCO3- µmol/kg ASW', 'CO32- µmol/kg ASW',
     'CO2 µmol/kg ASW', 'TCO2 µmol/kg ASW', 'g', 'µg',
     'N-concentration (µM)', 'P-concentration (µM)', 'Si-concentration (µM)',
     'Gross N-consumed (µM)', 'Gross P-consumed (µM)',
     'Gross Si-consumed (µM)', 'Dilution Rate (%)',
     'Target Culture Volume (mL)', 'Culture Before Dilution (mL)',
     '1) Media to Add (mL)', '2) Culture Discard (mL)',
     '3) Remaining Culture (mL)', '4) Media to Add (mL)',
     'Culture After Dilution (mL)',
     'Cell Density After Dilution (/mL)', 'EPI After Dilution (/mL)',
     'Fo after Dilution', 'Comments']]

    elif 'Nutrient' in path:
        return df[['Experiment', 'Variable', 'Species', 'Target N (µM)', 'Target P (µM)', 'Target Si (µM)', 'Incubator',
     'Date (dd/mm/yy)', 'Time (hh:mm:ss)', 'Experimental Day',
     'Hours (Between Sampling)',
     'Hours (Culturing Time)', 'n Cells (Pre-Dilution)', 'Pipette Volume (µl)', 'Magnification',
     'Mean Cell Width (µm)', 'Mean Cell Length (µm)', 'Cells/mL', 'Ln Cells',
     'Unnamed: 15 µ (d-1)', 'Unnamed: 16 Generations', 'NSV', 'NPQ', 'ρ',
     'σPII', 'αPII', 'τF', 'dρ', 'dσPII', 'dαPII', 'τS', 'Unnamed: 28 Fo', 'Unnamed: 29 Fm', 'Fv', 'Fv/Fm', 'Unnamed: 37 µ (d-1)',
     'Unnamed: 38 Generations', '(Free)', '°C', '(mg/L)', 'µatm', 'HCO3- µmol/kg ASW', 'CO32- µmol/kg ASW',
     'CO2 µmol/kg ASW', 'TCO2 µmol/kg ASW', 'g', 'µg', 'N-concentration (µM)', 'P-concentration (µM)', 'Si-concentration (µM)',
     'Gross N-consumed (µM)', 'Gross P-consumed (µM)', 'Gross Si-consumed (µM)',
     'Dilution Rate (%)', 'Target Culture Volume (mL)', 'Culture Before Dilution (mL)',
     '1) Media to Add (mL)',
     '2) Culture Discard (mL)', '3) Remaining Culture (mL)', '4) Media to Add (mL)',
     'Culture After Dilution (mL)',
     'Cell Density After Dilution (/mL)', 'Fo after Dilution', 'Comments']]


def get_dailies_cols_final(path):

    if 'Temp' in path:
        return ['Experiment', 'Variable', 'Species', 'Temperature', 'Incubator', 'Date (dd/mm/yy)', 'Time (hh:mm:ss)',
                'Experimental Day', 'Hours (Between Sampling)', 'Hours (Culturing Time)',
                'n Cells (Pre-Dilution)', 'Pipette Volume (µl)', 'Magnification', 'Mean Cell Width (µm)',
                'Mean Cell Length (µm)', 'Cells/mL', 'Ln Cells', 'µ (d-1) Nikon', 'Generations Nikon',
                'NSV', 'NPQ', 'ρ', 'σPII', 'αPII', 'τF', 'dρ', 'dσPII', 'dαPII', 'τS',
                'Fo', 'Fm', 'Fv', 'Fv/Fm', 'µ (d-1)', 'Generations', 'pH (Free)', 'Temperature (°C) measurements',
                'TA (mg/L)', 'pCO2 (µatm)', 'HCO3 (µmol/kg ASW)', 'CO3 (µmol/kg ASW)', 'CO2 (µmol/kg ASW)',
                'TCO2 (µmol/kg ASW)', 'Biomass (g)', 'Chl µg', 'Gross P-consumed (µM)', 'P concentration (µM)',
                'P concentration (µmol kg ASW)', 'Si concentration (µmol kg ASW)', 'Dilution Rate (%)',
                'Target Culture Volume (mL)', 'Culture Before Dilution (mL)', '1) Media to Add (mL)',
                '2) Culture Discard (mL)', '3) Remaining Culture (mL)', '4) Media to Add (mL)',
                'Culture After Dilution (mL)', 'Cell Density After Dilution (/mL)', 'Fo after Dilution', 'Comments'], ['P concentration (µmol kg ASW)', 'Si concentration (µmol kg ASW)']

    elif 'Light' in path:
        return ['Experiment', 'Variable', 'Species', 'Light', 'Incubator', 'Date (dd/mm/yy)', 'Time (hh:mm:ss)',
                'Experimental Day', 'Hours (Between Sampling)', 'Hours (Culturing Time)',
                'n Cells (Pre-Dilution)', 'Pipette Volume (µl)', 'Magnification', 'Mean Cell Width (µm)',
                'Mean Cell Length (µm)', 'Cells/mL', 'Ln Cells', 'µ (d-1) Nikon', 'Generations Nikon',
                'NSV', 'NPQ', 'ρ', 'σPII', 'αPII', 'τF', 'dρ', 'dσPII', 'dαPII', 'τS',
                'Fo', 'Fm', 'Fv', 'Fv/Fm', 'µ (d-1)', 'Generations', 'pH (Free)', 'Temperature (°C) measurements',
                'TA (mg/L)', 'pCO2 (µatm)', 'HCO3 (µmol/kg ASW)', 'CO3 (µmol/kg ASW)', 'CO2 (µmol/kg ASW)',
                'TCO2 (µmol/kg ASW)', 'Biomass (g)', 'Chl µg', 'Gross P-consumed (µM)', 'P concentration (µM)',
                'P concentration (µmol kg ASW)', 'Si concentration (µmol kg ASW)', 'Dilution Rate (%)',
                'Target Culture Volume (mL)', 'Culture Before Dilution (mL)', '1) Media to Add (mL)',
                '2) Culture Discard (mL)', '3) Remaining Culture (mL)', '4) Media to Add (mL)',
                'Culture After Dilution (mL)', 'Cell Density After Dilution (/mL)', 'Fo after Dilution', 'Comments'], ['P concentration (µmol kg ASW)', 'Si concentration (µmol kg ASW)']

    elif 'Nutrient' in path and 'IMS101' in path:
        return ['Experiment', 'Variable', 'Species', 'NaNO3', 'NaH2PO4', 'Na2SiO3',
                'Incubator', 'Date (dd/mm/yy)', 'Time (hh:mm:ss)',
                'Experimental Day', 'Hours (Between Sampling)', 'Hours (Culturing Time)',
                'n Cells (Pre-Dilution)', 'Pipette Volume (µl)', 'Magnification', 'Mean Cell Width (µm)',
                'Mean Cell Length (µm)', 'Cells/mL', 'Ln Cells', 'µ (d-1) Nikon', 'Generations Nikon',
                '∑EPI (Pre-Dilution)', 'Pipette Volume (µl) EPI', 'Magnification EPI', 'Mean Cell Width (µm) EPI',
                'Mean Cell Length (µm) EPI', '∑EPI/mL', 'Ln EPI', 'µ (d-1) EPI', 'Generations EPI',
                'NSV', 'NPQ', 'ρ', 'σPII', 'αPII', 'τF', 'dρ',
                'dσPII', 'dαPII', 'τS', 'Fo', 'Fm',
                'Fv', 'Fv/Fm', 'µ (d-1)', 'Generations', 'pH (Free)', 'Temperature (°C) measurements',
                'TA (mg/L)', 'pCO2 (µatm)', 'HCO3 (µmol/kg ASW)', 'CO3 (µmol/kg ASW)', 'CO2 (µmol/kg ASW)',
                'TCO2 (µmol/kg ASW)', 'Biomass (g)', 'Chl µg', 'Gross N-consumed (µM)', 'Gross P-consumed (µM)',
                'Gross Si-consumed (µM)', 'N-concentration (µM)', 'P-concentration (µM)', 'Si-concentration (µM)',
                'Dilution Rate (%)', 'Target Culture Volume (mL)',
                'Culture Before Dilution (mL)', '1) Media to Add (mL)', '2) Culture Discard (mL)',
                '3) Remaining Culture (mL)', '4) Media to Add (mL)', 'Culture After Dilution (mL)',
                'Cell Density After Dilution (/mL)', 'EPI After Dilution (/mL)', 'Fo after Dilution', 'Comments'], ['N-concentration (µM)', 'P-concentration (µM)', 'Si-concentration (µM)']

    elif 'Nutrient' in path:
        return ['Experiment', 'Variable', 'Species', 'NaNO3', 'NaH2PO4', 'Na2SiO3',
                'Incubator', 'Date (dd/mm/yy)', 'Time (hh:mm:ss)',
                'Experimental Day', 'Hours (Between Sampling)', 'Hours (Culturing Time)',
                'n Cells (Pre-Dilution)', 'Pipette Volume (µl)', 'Magnification', 'Mean Cell Width (µm)',
                'Mean Cell Length (µm)', 'Cells/mL', 'Ln Cells', 'µ (d-1) Nikon', 'Generations Nikon',
                'NSV', 'NPQ', 'ρ', 'σPII', 'αPII', 'τF', 'dρ', 'dσPII', 'dαPII', 'τS',
                'Fo', 'Fm', 'Fv', 'Fv/Fm', 'µ (d-1)', 'Generations', 'pH (Free)', 'Temperature (°C) measurements',
                'TA (mg/L)', 'pCO2 (µatm)', 'HCO3 (µmol/kg ASW)', 'CO3 (µmol/kg ASW)', 'CO2 (µmol/kg ASW)',
                'TCO2 (µmol/kg ASW)', 'Biomass (g)', 'Chl µg', 'Gross N-consumed (µM)', 'Gross P-consumed (µM)',
                'Gross Si-consumed (µM)', 'N-concentration (µM)', 'P-concentration (µM)', 'Si-concentration (µM)',
                'Dilution Rate (%)', 'Target Culture Volume (mL)',
                'Culture Before Dilution (mL)', '1) Media to Add (mL)', '2) Culture Discard (mL)',
                '3) Remaining Culture (mL)', '4) Media to Add (mL)', 'Culture After Dilution (mL)',
                'Cell Density After Dilution (/mL)', 'Fo after Dilution', 'Comments'], ['N-concentration (µM)', 'P-concentration (µM)', 'Si-concentration (µM)']
