import numpy as np
from scipy.stats import linregress
from math import floor

clean_slopes_labelled, clean_co2_slopes_labelled, labels = get_slopes_olc_co2(date, olc_date_path_dict, root, plot_dir, plotting)

oxy, t, labels, ph, regimes = get_data_olc_from_df(date, root)
pco2, bicarb, co3, co2, tco2 = clc(date, ph, olc_date_path_dict)

o2_slopes_labelled, co2_slopes_labelled = lc_slopes_split(oxy, t, co2, include_frac=0.2, plotting=plotting,
                                                          save_paths=save_paths, regimes=regimes, file_str=file_str)


def clean_label(label):
    label = label.replace('max', 'Max')
    label = label.replace('sub', 'Sub')
    label = label.replace('MA', 'Max')
    label = label.replace('SU', 'Sub')
    label = label.replace('-', ' ')

    if label == 'dakr':
        return 'Dark'
    elif label == '120 32Max':
        return '120 32 Max'
    else:
        return label.strip()


def olc_label_regimes(labels):
    regimes = []
    count = 0
    dk_count = 0
    for label in labels:
        if isinstance(label, str):
            if 'ark' in label:
                dk_count += 1
                label += str(dk_count)
            regimes.append([count, label])

        count += 1
    return regimes



def find_slope(x, y, include_frac):
    """
    Args:
        x: x-axis data
        y: y-axis data
        include_frac: minimal fraction of data to include in slope calculation
    Returns:
        slope: slope of optimal linear fit
        intercept: intercept of optimal linear fit
        r**2: r squared value, quality of fit

    """
    slope, intercept, r, p, se = linregress(x, y)
    start_index = 0
    fit_index = 0
    while start_index + floor(len(x) * include_frac) < len(x):
        new_slope, new_intercept, new_r, p, se = linregress(x[start_index:], y[start_index:])
        if new_r > r:
            slope, intercept, r, fit_index = new_slope, new_intercept, new_r, start_index

        start_index += 5

    return slope, intercept, r ** 2, fit_index, se


def lc_slopes_split(oxy, t, co2, include_frac, regimes):
    o2_slopes_labelled = {}
    co2_slopes_labelled = {}
    label_order = []
    count = 0
    for i in range(len(regimes)-1):
        label = regimes[i][1]
        label = clean_label(label)

        if 'ark' in label:
            label = f'Dark {count}'
            count += 1
        elif not label.replace(' ', '').isnumeric():
            continue

        label_order.append(label)

        t_segment = np.array(t[regimes[i][0]: regimes[i+1][0]])
        oxy_segment = np.array(oxy[regimes[i][0]: regimes[i + 1][0]])

        o2_slope, o2_intercept, o2_r_sq, start_index, se = find_slope(t_segment, oxy_segment, include_frac)
        co2_segment = np.array(co2[start_index + regimes[i][0]: regimes[i + 1][0]])
        x = t_segment[start_index:]
        co2_slope, co2_intercept, r, p, se = linregress(x, co2_segment)

        o2_slopes_labelled[label] = o2_slope
        o2_slopes_labelled[f'{label} error'] = se
        o2_slopes_labelled[f'{label} r-squared'] = o2_r_sq
        co2_slopes_labelled[label] = co2_slope
        co2_slopes_labelled[f'{label} error'] = se
        co2_slopes_labelled[f'{label} r-squared'] = r ** 2
        o2_slopes_labelled['Label order'] = label_order
        co2_slopes_labelled['Label order'] = label_order

    return o2_slopes_labelled, co2_slopes_labelled


def get_carbon_vals(ph, pcon, t_out, t_in, sicon = None, ta = None, tco2=None):
    pyco2_kws = {}

    # Define the known marine carbonate system parameters
    pyco2_kws["par1"] = ph  # pH measured in the lab, Total scale

    pyco2_kws["par1_type"] = 3  # tell PyCO2SYS: "par1 is a pH value"

    if tco2 is not None:
        pyco2_kws["par2"] = tco2  # DIC measured in the lab in μmol/kg-sw
        pyco2_kws["par2_type"] = 2  # tell PyCO2SYS: "par2 is a Total alkalinity value"
    elif ta is not None:
        pyco2_kws["par2"] = ta
        pyco2_kws["par2_type"] = 1  # tell PyCO2SYS: "par2 is a Total alkalinity value"

    # Define the seawater conditions and add them to the dict
    pyco2_kws["salinity"] = SALINITY  # practical salinity
    pyco2_kws["temperature"] = t_in  # lab temperature (input conditions) in °C
    pyco2_kws["temperature_out"] = t_out  # in-situ temperature (output conditions) in °C
    pyco2_kws["total_phosphate"] = pcon  # total phosphate in μmol/kg-sw
    if sicon is not None:
        pyco2_kws["total_silicate"] = sicon

    # Define PyCO2SYS settings and add them to the dict
    pyco2_kws["opt_pH_scale"] = 3  # tell PyCO2SYS: "the pH input is on the Free scale"
    pyco2_kws["opt_k_carbonic"] = 14  # tell PyCO2SYS: "use carbonate equilibrium constants of M10 (Millero 2010)"
    pyco2_kws["opt_k_bisulfate"] = 1  # tell PyCO2SYS: "use bisulfate dissociation constant of D90a"
    pyco2_kws["opt_total_borate"] = 2  # tell PyCO2SYS: "use borate:salinity of LKB10"

    # Now calculate everything with PyCO2SYS!
    results = pyco2.sys(**pyco2_kws)

    return results


def get_co2(phs, measurement_date, setr):
    ph, alkalinity, t_in, t_out, pcon, sicon = get_ph_alk_pcon_temp(setr) # create table,lookup based on SETR
    results = get_carbon_vals(ph=ph, pcon=pcon, t_in=t_out, t_out=t_out, ta=alkalinity, sicon=sicon)

    if measurement_date> datetime(2021, 5, 19):
        tco2 = results['dic']
        tco2 += BCSPIKE
        results = get_carbon_vals(ph=ph, pcon=pcon, t_in=t_out, t_out=t_out, tco2=tco2, sicon=sicon)
        ta = results['alkalinity']

    results = get_carbon_vals(ph=phs, pcon=pcon, t_in=t_out, t_out=t_out, ta=ta, sicon=sicon)
    tco2 = results['dic']
    return tco2
