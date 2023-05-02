BCSPIKE = 975.6097561
SALINITY = 30


Events = {'20/05/2021': 'Started adding BCSPIKE', '02/06/2021': 'Using O2/Spec Concentrate for FTIR sample',
          '10/06/2021': "Started filtering 100ml of culture for 'Chla - Culture' sample", '11/06/2021': 'STAF sensor switched to 010',
          '15/06/2021': 'Begin collecting samples for alkalinity measurements',
          '02/02/2022': ['Start 22degC M38', 'Start 26degC M38'],
          '19/04/2022': ['Start 18degC M38', 'Start 30degC M38'],
          '09/06/2022': 'Start 14degC M38',
          '14/06/2022': 'Start 34degC M38',
          '05/08/2022': ['Start 10degC M38', 'Start 38degC M38'],

}
 # 'C:/Users/XaviervanGorp/SuSeWi Ltd/Experimental Data - Documents/BACKUP/Data/'

##########
#  FTIR  #
##########

compounds = ['Protein', 'Protein', 'Protein', 'Protein', 'Protein', 'Protein', 'Protein', 'Carbohydrate', 'Carbohydrate', 'Carbohydrate', 'Carbohydrate', 'Carbohydrate', 'Carbohydrate', 'Carbohydrate', 'Fatty Acids', 'Fatty Acids', 'Fatty Acids', 'Fatty Acids', 'Fatty Acids', 'Fatty Acids', 'Fatty Acids', 'Fatty Acids', 'Fatty Acids', 'Saturated Lipids', 'Saturated Lipids', 'Saturated Lipids', 'Saturated Lipids', 'Saturated Lipids', 'Saturated Lipids', 'Saturated Lipids', 'Saturated Lipids', 'Saturated Lipids', 'Saturated Lipids', 'Polar Lipids', 'Polar Lipids', 'Polar Lipids', 'Polar Lipids', 'Polar Lipids', 'Nucleic Acids', 'Nucleic Acids', 'Si', 'Si', 'Si', 'Si', 'Si', 'Si', 'Si', 'Si', 'Si', 'Total Cells', 'Total Cells', 'Total Cells', 'Total Cells', 'Total Cells', 'Total Cells', 'Total Cells', 'Total Cells']
wl_text =['1410', '1540', '1550', '1990', '3070', '3270', '3310', '900-1200', '946', '997', '1032', '1070-1080', '1090', '1137', '725', '1228', '1653', '1740', '1743', '1752', '2245', '3010', '3012', '1054', '1080', '1377', '1380', '1458', '2920', '2925', '2933', '2955', '2970', '1096', '1100', '1155', '1187', '1240-1265', '1230-1250', '1240', '650', '1016', '1141', '1556', '1883', '2160', '2327', '3291', '3737', '607', '708', '1093', '1671', '2118', '2885', '3111', '3328']
wls = [[1410, 0], [1540, 0], [1550, 0], [1990, 0], [3070, 0], [3270, 0], [3310, 0], [900, 1200], [946, 0], [997, 0], [1032, 0], [1070, 1080], [1090, 0], [1137, 0], [725, 0], [1228, 0], [1653, 0], [1740, 0], [1743, 0], [1752, 0], [2245, 0], [3010, 0], [3012, 0], [1054, 0], [1080, 0], [1377, 0], [1380, 0], [1458, 0], [2920, 0], [2925, 0], [2933, 0], [2955, 0], [2970, 0], [1096, 0], [1100, 0], [1155, 0], [1187, 0], [1240, 1265], [1230, 1250], [1240, 0], [650, 0], [1016, 0], [1141, 0], [1556, 0], [1883, 0], [2160, 0], [2327, 0], [3291, 0], [3737, 0], [607, 0], [708, 0], [1093, 0], [1671, 0], [2118, 0], [2885, 0], [3111, 0], [3328, 0]]


clean_cols_3r6 = dict()
clean_cols_3r6['14'] = [0,1,2,3,6,7,8,14,15]
clean_cols_3r6['18'] = [0,1,2,3]
clean_cols_3r6['22'] = [6,7,8,9]
clean_cols_3r6['26'] = [12,13,14,15]
clean_cols_3r6['30'] = [12,13,14,15]

clean_cols_H = dict()
clean_cols_H['14'] = [0,1,2,3]
clean_cols_H['18'] = [0,1,2,3,6,7,8,9,12,13,14,15]
clean_cols_H['22'] = [0,1,2,3,6,7,8,9,12,13,14,15]
clean_cols_H['26'] = [6,7,8,9,12,13,14,15]
clean_cols_H['30'] = [12,13,14,15]


change_num = {2:6, 3:7, 4:8, 5:9}

growth_rates = {
                '3R6 T counts': [0.541, 0.743, 0.863, 0.970, 0.856],
                '3R6 T Fo': [0.554, 0.794, 1.017, 1.101, 1.046],
                'H T Fo': [0.181, 0.407, 0.434, 0.348, 0.366],
                'H T counts': [0.135, 0.321, 0.365, 0.366, 0.364]
                }


##########
#  kPAR  #
##########


kpar_depths = [1,5,10]

kpar_wls = [(442.2, 0), (492.1, 0), (559.0, 0), (664.9, 0), (703.8, 0), (739.1, 0), (779.7, 0), (431.7, 452.7), (459.1, 525.1), (541.0, 577.0), (649.4, 680.4), (695.8, 711.8), (731.6, 746.6), (769.7, 789.7), (441.5, 0), (490.0, 0), (531.0, 0), (565.0, 0), (610.0, 0), (665.0, 0), (705.0, 0), (431.0, 452.0), (465.0, 515.0), (513.0, 549.0), (547.0, 583.0), (600.0, 620.0), (650.0, 680.0), (697.0, 713.0)]
kpar_wls_text = ['442.2', '492.1', '559.0', '664.9', '703.8', '739.1', '779.7', '431.7-452.7', '459.1-525.1', '541.0-577.0', '649.4-680.4', '695.8-711.8', '731.6-746.6', '769.7-789.7', '441.5', '490.0', '531.0', '565.0', '610.0', '665.0', '705.0', '431.0-452.0', '465.0-515.0', '513.0-549.0', '547.0-583.0', '600.0-620.0', '650.0-680.0', '697.0-713.0']



range_dic = {'Si': [[650, 650], [1016, 1016], [1141, 1141], [1556, 1556], [1883, 1883], [2160, 2160], [2327, 2327], [3291, 3291], [3737, 3737]], 'Carbohydrate': [[900, 1200]], 'Protein': [[1410, 1410], [1540, 1540], [1550, 1550], [1990, 1990], [3070, 3070], [3270, 3270], [3310, 3310]], 'Polar Lipids': [[1096, 1096], [1100, 1100], [1155, 1155], [1187, 1187], [1240, 1265]], 'Nucleic Acids': [[1230, 1250]], 'Fatty Acids': [[725, 725], [1228, 1228], [1653, 1653], [1740, 1740], [1743, 1743], [1752, 1752], [2245, 2245], [3010, 3010], [3012, 3012]], 'Total Cells': [[607, 607], [708, 708], [1093, 1093], [1671, 1671], [2118, 2118], [2885, 2885], [3111, 3111], [3328, 3328]], 'Saturated Lipids': [[1054, 1054], [1080, 1080], [1377, 1377], [1380, 1380], [1458, 1458], [2920, 2920], [2925, 2925], [2933, 2933], [2955, 2955], [2970, 2970]]}

###############
# File struct #
###############

species = ['3R6', 'H', 'M38', 'IMS101']

species_names = ['Skeletonema', 'Dunaliella', 'Thalassiosira', 'Trichodesmium']

species_color_map = {'3R6': 'Red', 'H': 'Green', 'M38': 'Blue', 'IMS101': 'Black'}

experiments = ['Temperature', 'Light', 'Nutrients']

experiment_color_map = {'Temperature': 'Red', 'Nutrients': 'Green', 'Light': 'Blue'}

temps = [14, 18, 22, 26, 30, 34]

experiments_folders = ['1) Temperature Response', '2) Light Response', '3) Nutrient Response']

new_experiments_folders = ['01. Temperature', '02. Light', '03. Nutrients']

folder_map = {'Temperature': '01. Temperature', 'Light': '02. Light', 'Nutrients': '03. Nutrients', 'Growth_rates': '01. Growth Rates', 'STAF_Conversions': '02. LabSTAF Conversions', 'Growth_conditions': '03. Growth Conditions', 'Stoichiometry': '04. Stoichiometry', 'Absorption': '05. Light Absorption', 'KPAR': '06. KdPAR', 'FLC': "07. FLC's", 'OLC': "08. OLC's", 'CLC': "09. CLC's", 'FO2': "10. FO2's", 'FTIR': '11. FTIR', 'Nikon': '12. Nikon', 'Combined': 'x. Cross Analysis'}

experiments_folders_conversion = {k: v for k, v in zip(experiments_folders, new_experiments_folders)}

par_le_dict = {1120: 24.19, 704: 15.21, 430: 9.29, 249: 5.38, 130: 2.81, 52: 1.12}
pars = list(par_le_dict.keys())[::-1]

inc_nutrient_dict = {'NaNO3': 4,  'NaH2PO4': 5, 'Na2SiO3': 6}

nutrient_treats = [0.1, 0.2, 0.5, 1, 2, 5, 10, 15, 20, 50, 100, 400] # [f'{i}uM' for i in ]

nutrient_types = {'N': 'NaNO3', 'P': 'NaH2PO4', 'Si': 'Na2SiO3'}

TREAT_EXPERIMENT = {}
TREAT_EXPERIMENT['Temperature'] = temps
TREAT_EXPERIMENT['Light'] = pars
TREAT_EXPERIMENT['Nutrient levels'] = nutrient_treats
TREAT_EXPERIMENT['Nutrient types'] = list(nutrient_types.keys())
TREAT_EXPERIMENT['Nutrient sources'] = list(nutrient_types.values())

EXPERIMENT_UNITS = {}
EXPERIMENT_UNITS['Temperature'] = '°C'
EXPERIMENT_UNITS['Light'] = 'umol m2 s-1'
EXPERIMENT_UNITS['Nutrients'] = 'uM'

# incubator_to_treat_temp = {'1': 14, '2': 18, '3': 22, '4': 26, '5': 30, '6': 34}
incubator_to_treat_temp = {str(k+1):v for k, v in zip(range(6), temps)}
incubator_to_treat_light = {str(k+1):v for k, v in zip(range(6), pars)}
incubator_to_treat_nutrient = {'1': 'M38 Low temps', '2': 'M38 High temps', '3': 'Tricho', '4': 'N', '5': 'P', '6': 'Si'}
treat_to_inc_nutrient = new_dict = dict([(value, key) for key, value in incubator_to_treat_nutrient.items()])
nut_to_acid = {'N' : 'NaNO3', 'P' : 'NaH2PO4', 'Si' : 'Na2SiO3'}

###########
# Dailies #
###########

target_nutrients = ['Target N (µM)', 'Target P (µM)', 'Target Si (µM)']
M38_temp_dailies = {'14': '22', '18': '22', '22': '22', '26': '26', '30': '26', '34': '26', '38': '26', '10': '22', '12': '22'} #  {'22': [18.0, 22.0, 14.0], '26': [26.0, 30.0]}
M38_temp_inc = {'22': '1', '26': '2'}
inc_daily_col = {'1': 'Temperature (°C)', '2': 'Temperature (°C)', '3': 'Tricho', '4': 'Target N (µM)', '5': 'Target P (µM)', '6': 'Target Si (µM)'}

#######
# FLC #
#######

short_cols = ['E', 'rP', 'JVPII', 'GOPII', 'JPII', 'Fo', 'Fm', 'Fv/Fmc',
       "Fv'/Fmc'", "Fq'/Fv'", "AlphaPII", 'Rho', 'SigmaPII', 'TauES', 'Fo (dark)', 'Fm (dark)', 'Fv/Fmc (dark)',
       "Fv'/Fmc' (dark)", "AlphaPII (dark)", 'Rho (dark)', 'SigmaPII (dark)', 'TauES (dark)', 'rP (down)', 'JVPII (down)', 'GOPII (down)', 'JPII (down)', 'Fo (down)', 'Fm (down)', 'Fv/Fmc (down)',
       "Fv'/Fmc' (down)", "Fq'/Fv' (down)", "AlphaPII (down)", 'Rho (down)', 'SigmaPII (down)', 'TauES (down)']

long_cols = ['E', 'Fb', 'rP','rP fit', 'JVPII', 'GOPII', 'JPII', 'Fo', 'Fm', 'Fv/Fm','Fv/Fmc', "Fv'/Fmc'", "Fq'/Fv'", "Ekt'", "Ekt", "AlphaPII", 'SigmaPII', 'Rho', 'TauS', "TauEkt'", 'Fo (dark)', 'Fm (dark)', 'Fv/Fm (dark)', 'Fv/Fmc (dark)', "Fv'/Fmc' (dark)", "AlphaPII (dark)", 'SigmaPII (dark)', 'Rho (dark)', 'TauS (dark)', 'rP (down)', 'JVPII (down)', 'GOPII (down)', 'JPII (down)', 'Fo (down)', 'Fm (down)',  'Fv/Fm (down)', 'Fv/Fmc (down)', "Fv'/Fmc' (down)", "Fq'/Fv' (down)", "Ekt' (down)", "Ekt (down)", "AlphaPII (down)", 'SigmaPII (down)', 'Rho (down)', 'TauS (down)', "TauEkt (down)" ]

# M38_temp_dailies =  {'14': '22', '18': '22', '22': '22', '26': '26', '30': '26'} #  {'22': [18.0, 22.0, 14.0], '26': [26.0, 30.0]}


#########
#  OLC  #
#########

# olc_treatments = [29, 39, 368, 135, 72, 213, 574, 2000, 229, 105, 393, 879, 1331, 'Dark']
# sorted olc treatments
olc_treatments = [29, 39, 72, 105, 135, 213, 229, 368, 393, 574, 879, 1331, 2000]
# dictionary of treatments and weight used for fitting
olc_treatment_weights = {29: 0.1, 39: 0.1, 72: 0.1, 105: 0.1, 135: 0.1, 213: 0.1, 229: 0.1, 368: 0.2, 393: 0.2, 574: 0.3, 879: 0.5, 1331: 0.5, 2000: 0.7}

#########
#  FO2  #
#########

fo2_treatments = ['120 40 Max', '120 32 Max', '120 25 Max', '120 25 Sub']
fo2_frequencies = {'120 40 Max': 1000/40, '120 32 Max': 1000/32, '120 25 Max': 1000/25, '120 25 Sub': 1000/25}

############
#  (S)PAR  #
############
spar_spec_cols = [str(i) for i in range(340, 821)]
spar_wl = [i for i in range(340, 821)]


#########
# NIKON #
#########

all_cols = ['EqDiameter', 'MaxFeret', 'Circularity', 'Perimeter', 'MeanObjIntensity', 'ObjectArea', 'MinFeret'] #'VolumeEqSphere',

all_wells = ['A01', 'A02', 'A03', 'A04', 'A05', 'A06', 'B01', 'B02', 'B03', 'B04', 'B05', 'B06', 'D01', 'D02', 'D03', 'D04', 'D05', 'D06', 'E01', 'E02', 'E03', 'E04', 'E05', 'E06', 'G01', 'G02', 'G03', 'G04', 'G05', 'G06', 'H01', 'H02', 'H03', 'H04', 'H05', 'H06']


def well_to_details(folder_source, well):
    found = True
    if 'A' in well:
        species = 'M38'
        dilution = 0

    if 'D' in well:
        species = 'H'
        dilution = 50

    if 'G' in well:
        species = '3R6'
        dilution = 80

    if 'B' in well:
        species = 'M38'
        dilution = 50

    if 'E' in well:
        species = 'H'
        dilution = 80

    if 'H' in well:
        species = '3R6'
        dilution = 90

    if 'emp' in folder_source:
        experiment = 'Temperature'
        treatment = incubator_to_treat_temp[well[-1]]
        true_experiment = folder_map[experiment]

    elif 'ight' in folder_source:
        experiment = 'Light'
        treatment = incubator_to_treat_light[well[-1]]
        true_experiment = folder_map[experiment]

    elif 'utrient' in folder_source:
        experiment = 'Nutrients'
        treatment = incubator_to_treat_nutrient[well[-1]]
        true_experiment = folder_map[experiment]
        if species == 'M38':
            if well[-1] in ['1', '2']:
                true_experiment = '01. Temperature'

    else:
        print('bad experiment folder', folder_source)
        found = False

    if found:
        return experiment, species, treatment, true_experiment, dilution


#########
#  FAM  #
#########

culture_data_cols = ['Dates', 'Time', 'Culturing Time (h)', 'Measurement', 'Pond level',
       'Culture Volume (L)', 'Cell density (/mL)', 'Growth rate (d-1)',
       'Cells Evolution (%)', 'Dilution %', 'Dilution (%) with Min Threshold',
       'Seawater to add (L)', 'Added Nutrients     N (ml)',
       'Added Nutrients          P (ml)',
       'Type and Percentage Of Contaminants',
       'Culture Temperature at Peak (°C)',
       'Light Intensity (µmol photons m-2 s-1)', 'pH B.D', 'pH A.D',
       'Bubbled (Yes/No)', 'Time of dilution', 'Media Type']


fam_ponds = ['12D', '12O', '13D', '13O', '14D', '14O', '15D', '15O']
cells_biomass = {'3R6': 3.445305770887163 * 10**(-5), 'H': 0.0002683057710132231, 'M38': 0.00017382527755972315}




# nature/physics
DENSITY_WATER = 1.025
MOLECULES = {'C': {'molecular_weight': 12.0107},
             'CO2': {'molecular_weight': 44.009}}
OFFSET_KELVIN = 273.15
REFR_INDEX_AIR = 1.00029
REFR_INDEX_WATER = 1.333
ATMOSPHERIC_CO2 = 422 * 10**(-6)

# maths
EPS = 1e10

# mass/volume
ML_PER_LITRE = 1000
LITRES_PER_M3 = 1000
G_PER_KG = 1000
KG_PER_T = 1000
MICROMOL_PER_MOL = 1000000
MILLIMOL_PER_MOL = 1000


# trigonometry
CIRCLE_QUAR_DEG = 90
CIRCLE_HALF_DEG = 180
CIRCLE_FULL_DEG = 360
RAD_PER_DEG = np.pi/CIRCLE_HALF_DEG

# geometry
LAT = 28.146083
LON = -12.136694

# time
HOURS_PER_DAY = 24
MINUTES_PER_DAY = 1440
MINUTES_PER_HOUR = 60
SECONDS_PER_DAY = 86400
SECONDS_PER_HOUR = 3600
SECONDS_PER_MINUTE = 60
JULIAN_CENTURY = 36525
JULIAN_EPOCH = 2451545
TZ = 0

#Photosynthetic constants
ELECTRONS_PER_OXYGEN = 4

