import pandas as pd
import xlrd
import matplotlib
import numpy as np
import const as ct
import re

def normalizeWage(colWage, colUnit, dataframe):
    dataframe[colWage] = dataframe.apply(lambda row: row[colWage] * ct.FACTORS_UNITS[ct.UNITS.index(row[colUnit])], axis=1)
    dataframe = dataframe.drop([colUnit], axis=1)

def H1Bdata(i):
    df = pd.read_excel(ct.PATH_H1B + str(ct.YEARS[i]) + ct.EXT_ORI, index_col=None)
    df = df[ct.COLUMNS_YEAR_H1B[i]]
    df.columns = ct.COLUMNS_H1B
    df['YEAR'] = ct.YEARS[i]
    df_h1b = df.loc[df['VISA'] == 'H-1B']

    len_ori = len(df_h1b)

    for col in ct.COLUMNS_H1B:
        df_h1b = df_h1b.loc[df_h1b[col].notnull()]

    len_to = len(df_h1b)
    print(str(len_ori - len_to) + "/" + str(len_ori) + " rows with missing values removed for year " + str(ct.YEARS[i]))

    # for the case such as "8000 -", "6000 - 8000", and other
    df_h1b['WAGE'] = df_h1b.apply(
        lambda row: row['WAGE'].split("-", 1)[0].strip()
        if isinstance(row['WAGE'], str)
           and "-" in row['WAGE']
        else row['WAGE'], axis=1)

    df_h1b['WAGE'] = df_h1b['WAGE'].astype(float)
    df_h1b['WAGE'] = df_h1b['WAGE'].astype(int)

    len_to2 = len(df_h1b)
    print(
        str(len_to - len_to2) + "/" + str(len_ori) + " rows with non-numberic values removed for year " + str(ct.YEARS[i]))

    df_h1b.to_csv(ct.PATH_H1B + str(ct.YEARS[i]) + "_before" + ct.EXT_TO, index=False)

    # normalize wage
    normalizeWage('WAGE', 'WAGE_UNIT', df_h1b)
    normalizeWage('PW', 'PW_UNIT', df_h1b)
    df_h1b = df_h1b.drop(['WAGE_UNIT'], axis=1)
    df_h1b = df_h1b.drop(['PW_UNIT'], axis=1)
    df_h1b['WAGE'] = df_h1b['WAGE'].astype(int)
    df_h1b['PW'] = df_h1b['WAGE'].astype(int)
    df_h1b['TOTAL'] = df_h1b['TOTAL'].astype(int)

    df_h1b = df_h1b.drop(['VISA'], axis=1)
    df_h1b.to_csv(ct.PATH_H1B + str(ct.YEARS[i]) + ct.EXT_TO, index=False)
    return df_h1b

def getOccupation(row):
    if isinstance(row['SOC_CODE'], str):
        if "-" in row['SOC_CODE'] or "." in row['SOC_CODE']:
            strOccu = re.split("-|\.", row['SOC_CODE'])[0]
            if strOccu == "Nov":
                return 11
            else:
                return float(strOccu)
    return float(row['SOC_CODE'])

def getMap2(list1, list2):
    res = {}
    for i in range(len(list1)):
        res[list1[i]] = i
        res[list2[i]] = i
    return res

def getMap1(list):
    res = {}
    for i in range(len(list)):
        res[list[i]] = i
    return res

def getDroplistOccupation(soccode):
    res = []
    for x in soccode:
        if isinstance(x, str):
            if "-" in x or "." in x:
                #if re.split("-|\.", x)[0].isnumeric():
                continue
                # else:
                #     res.append(x)
            else:
                if not x.isnumeric():
                    res.append(x)
    res.append(None)
    return res

def getDroplistWage(wage):
    res = []
    for x in wage:
        if isinstance(x, str):
            if isfloat(x):
                continue
            else:
                res.append(x)
    res.append(None)
    return res

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

def PWD(i):
    df = pd.read_excel(ct.PATH_PWD + str(ct.YEARS[i]) + ct.EXT_ORI, index_col=None)
    df = df[ct.COLUMNS_YEAR_PWD[i]]
    df.columns = ct.COLUMNS_PWD
    df['YEAR'] = ct.YEARS[i]
    df_pwd = df.loc[df['VISA'] == 'H-1B']

    len_ori = len(df_pwd)

    for col in ct.COLUMNS_PWD:
        df_pwd = df_pwd.loc[df_pwd[col].notnull()]

    len_to = len(df_pwd)
    print(str(len_ori - len_to) + "/" + str(len_ori) + " rows with missing values removed for year " + str(ct.YEARS[i]))

    # for the case such as "8000 -", "6000 - 8000", and other
    df_pwd['WAGE'] = df_pwd.apply(
        lambda row: row['WAGE'].split("-", 1)[0].strip()
        if isinstance(row['WAGE'], str)
           and "-" in row['WAGE']
        else row['WAGE'], axis=1)

    df_pwd['WAGE'] = df_pwd['WAGE'].astype(float)
    df_pwd['WAGE'] = df_pwd['WAGE'].astype(int)

    len_to2 = len(df_pwd)
    print(
        str(len_to - len_to2) + "/" + str(len_ori) + " rows with non-numberic values removed for year " + str(
            ct.YEARS[i]))

    df_pwd.to_csv(ct.PATH_PWD + str(ct.YEARS[i]) + "_before" + ct.EXT_TO, index=False)

    # normalize wage
    normalizeWage('WAGE', 'WAGE_UNIT', df_pwd)
    df_pwd = df_pwd.drop(['WAGE_UNIT'], axis=1)
    df_pwd['WAGE'] = df_pwd['WAGE'].astype(int)

    df_pwd = df_pwd.drop(['VISA'], axis=1)
    df_pwd.to_csv(ct.PATH_PWD + str(ct.YEARS[i]) + ct.EXT_TO, index=False)
    return df_pwd

def PERM(i):
    df = pd.read_excel(ct.PATH_PERM + str(ct.YEARS[i]) + ct.EXT_ORI, index_col=None)
    df = df[ct.COLUMNS_YEAR_PERM[i]]
    df.columns = ct.COLUMNS_PERM
    df['YEAR'] = ct.YEARS[i]
    df_perm = df.loc[df['VISA'] == 'H-1B']

    len_ori = len(df_perm)

    for col in ct.COLUMNS_PERM:
        df_perm = df_perm.loc[df_perm[col].notnull()]

    len_to = len(df_perm)
    print(str(len_ori - len_to) + "/" + str(len_ori) + " rows with missing values removed for year " + str(ct.YEARS[i]))

    # for the case such as "8000 -", "6000 - 8000", and other
    df_perm['WAGE'] = df_perm.apply(
        lambda row: row['WAGE'].split("-", 1)[0].strip()
        if isinstance(row['WAGE'], str)
           and "-" in row['WAGE']
        else row['WAGE'], axis=1)

    # for the case such as "98,000.00“
    df_perm['WAGE'] = df_perm['WAGE'].apply(
        lambda x: x.replace(',', '').strip()
        if isinstance(x, str) else x)
    droplistWage = getDroplistWage(df_perm.WAGE)
    print(droplistWage)
    df_perm = df_perm[~df_perm['WAGE'].isin(droplistWage)]
    df_perm['WAGE'] = df_perm['WAGE'].astype(float)
    df_perm['WAGE'] = df_perm['WAGE'].astype(int)

    len_to2 = len(df_perm)
    print(
        str(len_to - len_to2) + "/" + str(len_ori) + " rows with non-numberic values removed for year " + str(
            ct.YEARS[i]))

    df_perm.to_csv(ct.PATH_PWD + str(ct.YEARS[i]) + "_before" + ct.EXT_TO, index=False)

    # normalize wage
    normalizeWage('WAGE', 'WAGE_UNIT', df_perm)
    df_perm = df_perm.drop(['WAGE_UNIT'], axis=1)
    df_perm['WAGE'] = df_perm['WAGE'].astype(int)

    df_perm = df_perm.drop(['VISA'], axis=1)
    df_perm.to_csv(ct.PATH_PERM + str(ct.YEARS[i]) + ct.EXT_TO, index=False)
    return df_perm

def getDataPWD():

    dfs = []
    for i in range(5):
        dfs.append(PWD(i))
    dfH1B = pd.concat(dfs)
    dfH1B.to_csv(ct.PATH_PWD + "merged" + ct.EXT_TO, index=False)

def getDataPERM():

    dfs = []
    for i in range(5):
        dfs.append(PERM(i))
    dfPERM = pd.concat(dfs)
    dfPERM.to_csv(ct.PATH_PERM + "merged" + ct.EXT_TO, index=False)

def numeric(filepath, statuses):
    df = pd.read_csv(filepath + "merged" + ct.EXT_TO, low_memory=False)

    # Numeric occupation
    droplistOccupation = getDroplistOccupation(df.SOC_CODE)
    print(droplistOccupation)
    df = df[~df['SOC_CODE'].isin(droplistOccupation)]
    df['OCCUPATION'] = df.apply(lambda row: getOccupation(row), axis=1)
    df['OCCUPATION'] = df['OCCUPATION'].astype(int)

    # Numeric state
    print(df[~(df['STATE'].isin(ct.STATES + ct.STATES_FULL))].STATE)
    df = df[df['STATE'].isin(ct.STATES + ct.STATES_FULL)]
    mapState = getMap2(ct.STATES, ct.STATES_FULL)
    df = df.replace({'STATE': mapState})

    # Numberic status
    mapStatus = getMap1(statuses)
    df = df.replace({'STATUS': mapStatus})

    df.to_csv(filepath + "numeric" + ct.EXT_TO, index=False)

def numericEducation(filepath):
    df = pd.read_csv(filepath + "numeric" + ct.EXT_TO, low_memory=False)

    # Numeric education
    mapEducation = getMap1(ct.EDUCATION)
    df = df.replace({'EDUCATION': mapEducation})

    df.to_csv(filepath + "numeric" + ct.EXT_TO, index=False)

def getDataH1b():
    dfs = []
    for i in range(5):
        dfs.append(H1Bdata(i))
    dfH1B = pd.concat(dfs)
    dfH1B.to_csv(ct.PATH_H1B + "merged" + ct.EXT_TO, index=False)

# getDataH1b()
# numeric(ct.PATH_H1B, ct.STATUS_H1B)

# getDataPWD()
# numeric(ct.PATH_PWD, ct.STATUS_PWD)
#numericEducation(ct.PATH_PWD)

# getDataPERM()
# numeric(ct.PATH_PERM, ct.STATUS_PERM)

#TODO numeric PERM's citizenship: probably not, too many countries