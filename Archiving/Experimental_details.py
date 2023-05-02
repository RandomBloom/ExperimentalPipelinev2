import numpy as np
import pandas as pd
from archiving_tools import root_data_dir, get_full_treat_info


def update_exp_details():
    e_dtls = pd.read_excel(f"{root_data_dir.replace('/01. Primary Productivity', '')}/Experimental Details (TO FILL OUT).xlsx")
    to_pop = []
    for idx, row in e_dtls.iterrows():
        e_dtls.loc[idx, 'Treatment'] = str(row['Treatment']).replace('°C', '').replace('C', '')
        try:
            pd.to_datetime(row['Date'])
        except Exception as e:
            print(e, row['Date'])
            to_pop.append(idx)
    df = e_dtls.drop(index=to_pop)
    df['Datetime'] = pd.to_datetime(df['Date'])
    new_dates = [str(i).split(' ')[0].split('-') for i in df['Datetime']]
    df['Date (dd/mm/yy)'] = [f'{i[2]}/{i[1]}/{i[0][2:]}' if len(i) == 3 else np.nan for i in new_dates]
    df.dropna(thresh=3, axis=0, inplace = True)

    exp_dtls = df.copy()

    exp_dtls.loc[exp_dtls.Species == 101, 'Species'] = 'IMS101'

    full_treat_infos = []
    for treat_str, species, experiment in zip(exp_dtls.Treatment, exp_dtls.Species, exp_dtls.Experiment):
        full_treat_infos.append(get_full_treat_info(treat_str, species, experiment))

    all_keys = set()
    for i in full_treat_infos:
        all_keys = all_keys.union(set(i.keys()))
    print(all_keys)
    for k in full_treat_infos[0].keys():
        exp_dtls[k] = [i[k] for i in full_treat_infos]

    exp_dtls.rename(columns={'Unnamed: 4': 'Good Exp'}, inplace=True)
    exp_dtls.Keep = exp_dtls['Good Exp'].fillna(1.0)
    exp_dtls.loc[exp_dtls.NaH2PO4 == 43.0, 'NaH2PO4'] = 43.4

    return exp_dtls

    # exp_dtls.to_parquet()


# exp_dtls = update_exp_details()
