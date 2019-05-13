DATAPATH = 'data/BudgetItaly.csv'
COL_NAMES = ["wfood","whouse","wmisc","pfood","phouse","pmisc","totexp","year","income","size","pct"]
# K = 3
# DATA_FRAC = 0.5

PATH_H1B = 'data\H-1B_'
EXT_ORI = '.xlsx'
EXT_TO = '.csv'

STATES = ["AK","AL","AR","AZ","CA","CO","CT","DC","DE","FL","GA","GU","HI","IA","ID", "IL","IN","KS","KY","LA","MA","MD","ME","MH","MI","MN","MO","MS","MT","NC","ND","NE","NH","NJ","NM","NV","NY", "OH","OK","OR","PA","PR","PW","RI","SC","SD","TN","TX","UT","VA","VI","VT","WA","WI","WV","WY"]
STATUS = ['CERTIFIED-WITHDRAWN', 'CERTIFIED', 'DENIED', 'WITHDRAWN', 'REJECTED']
YEARS = [2014, 2015, 2016, 2017, 2018]

NUM_COLUMN_H1B = 11

COLUMNS_H1B = [
    'STATUS',
    'VISA',
    'EMPLOYER',
    'CITY',
    'STATE',
    'TOTAL',
    'SOC_CODE',
    'SOC_NAME',
    'JOB_TITLE',
    'WAGE',
    'WAGE_UNIT',
    'PW',
    'PW_UNIT']

YEARS = [2014, 2015, 2016, 2017, 2018]
COLUMNS = [
    # 2014
    ['STATUS',
    'VISA_CLASS',
    'LCA_CASE_EMPLOYER_NAME',
    'LCA_CASE_EMPLOYER_CITY',
    'LCA_CASE_EMPLOYER_STATE',
    'TOTAL_WORKERS',
    'LCA_CASE_SOC_CODE',
    'LCA_CASE_SOC_NAME',
    'LCA_CASE_JOB_TITLE',
    'LCA_CASE_WAGE_RATE_FROM',
    'LCA_CASE_WAGE_RATE_UNIT',
    'PW_1',
    'PW_UNIT_1'],
    # 2015
    ['CASE_STATUS',
    'VISA_CLASS',
    'EMPLOYER_NAME',
    'EMPLOYER_CITY',
    'EMPLOYER_STATE',
    'TOTAL WORKERS',
    'SOC_CODE',
    'SOC_NAME',
    'JOB_TITLE',
    'WAGE_RATE_OF_PAY',
    'WAGE_UNIT_OF_PAY',
    'PREVAILING_WAGE',
    'PW_UNIT_OF_PAY'],
    # 2016
    ['CASE_STATUS',
    'VISA_CLASS',
    'EMPLOYER_NAME',
    'EMPLOYER_CITY',
    'EMPLOYER_STATE',
    'TOTAL_WORKERS',
    'SOC_CODE',
    'SOC_NAME',
    'JOB_TITLE',
    'WAGE_RATE_OF_PAY_FROM',
    'WAGE_UNIT_OF_PAY',
    'PREVAILING_WAGE',
    'PW_UNIT_OF_PAY'],
    # 2017
    ['CASE_STATUS',
     'VISA_CLASS',
    'EMPLOYER_NAME',
    'EMPLOYER_CITY',
    'EMPLOYER_STATE',
    'TOTAL_WORKERS',
    'SOC_CODE',
    'SOC_NAME',
    'JOB_TITLE',
    'WAGE_RATE_OF_PAY_FROM',
    'WAGE_UNIT_OF_PAY',
    'PREVAILING_WAGE',
    'PW_UNIT_OF_PAY'],
    # 2018
    ['CASE_STATUS',
     'VISA_CLASS',
    'EMPLOYER_NAME',
    'EMPLOYER_CITY',
    'EMPLOYER_STATE',
    'TOTAL_WORKERS',
    'SOC_CODE',
    'SOC_NAME',
    'JOB_TITLE',
    'WAGE_RATE_OF_PAY_FROM',
    'WAGE_UNIT_OF_PAY',
    'PREVAILING_WAGE',
    'PW_UNIT_OF_PAY']
]

# for index, row in df.iterrows():
UNITS = ['Year', 'Month', 'Bi-Weekly', 'Week', 'Hour']
FACTORS_UNITS = [1, 12, 27, 54, 2160]