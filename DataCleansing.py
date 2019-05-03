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
    df = df[ct.COLUMNS[i]]
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
            return float(re.split("-|\.", row['SOC_CODE'])[0])
    return float(row['SOC_CODE'])

def getMap(list):
    res = {}
    for i in range(len(list)):
        res[list[i]] = i
    return res

def getDroplistOccupation(soccode):
    res = []
    for x in soccode:
        if isinstance(x, str):
            if "-" in x or "." in x:
                continue
            else:
                if not x.isnumeric():
                    res.append(x)
    res.append(None)

def main():
    dfH1B = pd.read_csv(ct.PATH_H1B + "merged" + ct.EXT_TO, low_memory=False)
    dfH1B = dfH1B[~dfH1B['SOC_CODE'].isin(ct.DROP_SOCCODE)]
    dfH1B['OCCUPATION'] = dfH1B.apply(lambda row: getOccupation(row), axis=1)
    dfH1B['OCCUPATION'] = dfH1B['OCCUPATION'].astype(int)

    dfs = []
    for i in range(5):
        dfs.append(H1Bdata(i))
    dfH1B = pd.concat(dfs)
    dfH1B.to_csv(ct.PATH_H1B + "merged" + ct.EXT_TO, index=False)



def numeric():
    dfH1B = pd.read_csv(ct.PATH_H1B + "merged" + ct.EXT_TO, low_memory=False)

    # Numeric occupation
    droplistOccupation = getDroplistOccupation()
    dfH1B = dfH1B[~dfH1B['SOC_CODE'].isin(droplistOccupation)]
    dfH1B['OCCUPATION'] = dfH1B.apply(lambda row: getOccupation(row), axis=1)
    dfH1B['OCCUPATION'] = dfH1B['OCCUPATION'].astype(int)

    # Numeric state
    dfH1B = dfH1B[dfH1B['STATE'].isin(ct.STATES)]
    mapState = getMap(ct.STATES)
    dfH1B = dfH1B.replace({'STATE': mapState})

    # Numberic status
    mapStatus = getMap(ct.STATUS)
    dfH1B = dfH1B.replace({'STATUS': mapStatus})

    dfH1B.to_csv(ct.PATH_H1B + "numeric" + ct.EXT_TO, index=False)

#numeric()