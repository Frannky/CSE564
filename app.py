import json

from flask import Flask, render_template, request, redirect, Response, jsonify, url_for
import pandas as pd
import numpy as np
import random as rd
import sklearn as sl
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
from sklearn.manifold import MDS
import const as ct
import string

#dataRaw
#dataRandom
#dataStratified

#First of all you have to import it from the flask module:
app = Flask(__name__)
#By default, a route only answers to GET requests. You can use the methods argument of the route() decorator to handle different HTTP methods.
@app.route("/", methods = ['POST', 'GET'])
def index():
    #df = pd.read_csv('data.csv').drop('Open', axis=1)
    global dataH1B
    global dataPWD
    global dataPERM
    global dataEmployerPartition

    data = dataH1B

    #The current request method is available by using the method attribute
    if request.method == 'POST':
        # KMeans: k <- 3
        if request.form['data'] == 'corrMatrix':
            data = data.corr()
        elif request.form['data'] == 'covMatrix':
            data = data.cov()
        elif request.form['data'] == 'EmployerPeitionRank':
            nEmployerPartition= 3
            data = getEmployerPartitionForYear(dataEmployerPartition, nEmployerPartition)
        else:
            print("wrong data request")
            return

        chart_data = data.to_dict(orient='records')
        chart_data = json.dumps(chart_data, indent=2)
        data = {'chart_data': chart_data}
        # data = {'chart_data': chart_data}
        return jsonify(data) # Should be a json string

    elif request.method == 'GET':
        # data = data[['STATUS','YEAR']]
        # data = data.rename(columns={'STATES':'x', 'YEAR': 'y'})
        chart_data = {'x': [1, 2], 'y': [3, 4]}
        # chart_data = data.to_dict(orient='records')
        chart_data = json.dumps(chart_data, indent=2)
        data = {'chart_data': chart_data}
        return render_template("index.html", data=data)

# @app.route("/member", methods = ['POST', 'GET'])
# def index():
    ###

@app.route("/gridmap/<string:chartname>", methods = ['POST', 'GET'])
def gridmap(chartname):
    variables = chartname.split(' ')
    category = "none"
    data = []
    dataDomain = []
    categories = []
    categoryName = "none"
    if len(variables) > 1:
        chartname = variables[0]
        category = variables[1]
        categoryId = int(variables[2])

    if chartname == "MeanWage":
        chartname = "Mean Wage"
        if category == "none":
            groups = (dataH1B.groupby('STATE').mean().WAGE).round(2)
            data = json.dumps(groups.to_dict(), indent=2)
            dataDomain = [0, 375000, 750000, 1125000, 1500000]
        elif category == "OCCUPATION":
            categories = list(ct.OCCUPATION.keys())
            categoryVal = categories[categoryId]
            categoryName = ct.OCCUPATION[categoryVal] + " Occupation"
            categories = list(ct.OCCUPATION.values())
            groups = (dataH1B[dataH1B[category] == categoryVal].groupby('STATE').mean().WAGE).round(2)
            data = json.dumps(groups.to_dict(), indent=2)
            for i in range(5):
                dataDomain.append(i * int(round(groups.max() / 4, -4)))
        elif category == "YEAR":
            categories = ct.YEARS.keys()
            categoryVal = categories[categoryId]
            categoryName = ct.YEARS[categoryVal] + " Occupation"
            groups = (dataH1B[dataH1B[category] == ct.YEARS[categoryId]].groupby(
                'STATE').mean().WAGE).round(2)
            data = json.dumps(groups.to_dict(), indent=2)
            for i in range(5):
                dataDomain.append(i * int(round(groups.max() / 4, -4)))
    elif chartname == "TotalPetitions":
        chartname = "Total Petitions"
        if category == "none":
            total = dataH1B.groupby('STATE').size()
            resdata = json.dumps(total.tolist(), indent=2)
            dataDomain = [0, 125000, 250000, 375000, 500000]
    else:
        data = []
    data = {'chart_data': data}
    data['dataname'] = "'" + chartname + "'"
    data['states'] = ct.STATES
    data['domain'] = dataDomain
    data['category'] = "'" + category + "'"
    data['categories'] = categories
    data['categoryname'] = "'" + categoryName + "'"
    return render_template('gridmap.html', data=data)

@app.route("/heatmap/<int:data_id>", methods = ['POST', 'GET'])
def heatmap(data_id):
    if data_id == 0:
        data = dataH1B.corr()
    elif data_id == 1:
        data = dataPWD.corr()
    elif data_id == 2:
        data = dataPERM.corr()

    dataHeatmap = pd.DataFrame(columns=['x', 'y', 'value'])

    index = 0
    for x, values in data.iteritems():
        for y, value in values.iteritems():
            dataHeatmap.loc[index] = [x, y, value]
            index = index + 1

    chart_data = dataHeatmap.to_dict(orient='records')
    chart_data = json.dumps(chart_data, indent=2)
    group_data = json.dumps(data.columns.tolist(), indent=2)

    data = {'chart_data': chart_data}
    data['group_data'] = group_data

    return render_template('heatmap.html', data=data)

@app.route("/barchart", methods = ['POST', 'GET'])
def barchart():
    data = dataH1B.groupby(['STATE']).size().to_frame("y")
    data["x"] = data.index
    chart_data = data.to_dict(orient='records')
    chart_data = json.dumps(chart_data, indent=2)
    data = {'chart_data': chart_data}
    return render_template('barchart.html', data=data)

@app.route("/stackedbarchart/<string:chartname>", methods=['POST', 'GET'])
def stackedbarchart(chartname):
    if chartname == "Petition By Education":
        removeCategory = dataPWD.groupby('EDUCATION').size().nsmallest(3).index
        dataToMerge, group = mergeOther(dataPWD.copy(), ct.EDUCATION, removeCategory, 'EDUCATION')

        data = dataToMerge.groupby('YEAR').EDUCATION.apply(pd.value_counts)

        res = pd.DataFrame(columns=group)
        index = 0
        for x in ct.YEARS:
            row = []
            for g in range(len(group)):
                row.append(data[x][g])
            res.loc[x] = row
        res['x'] = res.index
        res['total'] = dataToMerge.groupby('YEAR').size()

        data = res
        dataGroup = group
        dataX = ct.YEARS

    chart_data = data.to_dict(orient='records')
    chart_data = json.dumps(chart_data, indent=2)
    group_data = json.dumps(dataGroup, indent=2)
    x_data = json.dumps(dataX, indent=2)
    data = {'chart_data': chart_data}
    data['group_data'] = group_data
    data['x_data'] = x_data
    return render_template('stackedbarchart.html', data=data)

@app.route("/piechart/<int:data_id>", methods = ['POST', 'GET'])
def piechart(data_id):
    if data_id == 0:
        data = dataPWD.groupby(['EDUCATION']).size().to_frame("y")
        data["x"] = data.index
    elif data_id == 1:
        values = dataPWD.groupby('EDUCATION').YEAR.apply(pd.value_counts)
        dataPetition = pd.DataFrame(columns=['education', 'year', 'value'])
        index = 0
        for x, value in values.iteritems():
            dataPetition.loc[index] = [x[0], x[1], value]
            index = index + 1
        data = dataPetition

    chart_data = data.to_dict(orient='records')
    chart_data = json.dumps(chart_data, indent=2)
    data = {'chart_data': chart_data}
    return render_template('piechart.html', data=data)

def mergeOther(dataOri, oriCategory, removeCategory, colname):
    data = dataOri
    newCategory = list(set(range(len(oriCategory))) - set(removeCategory))
    newCategoryName = np.array(oriCategory)[newCategory].tolist()
    newCategoryName.append("Other")

    newCategoryMap = {}
    for old in range(len(oriCategory)):
        if old in newCategory:
            newCategoryMap[old] = newCategory.index(old)
        else:
            newCategoryMap[old] = len(newCategory)

    data[colname] = data[colname].map(newCategoryMap)
    return [data, newCategoryName]


@app.route("/scatterplot/<string:chartname>", methods = ['POST', 'GET'])
def scatterplot(chartname):
    if chartname == "Petition By Education":
        removeCategory = dataPWD.groupby('EDUCATION').size().nsmallest(3).index
        dataToMerge, group = mergeOther(dataPWD.copy(), ct.EDUCATION, removeCategory, 'EDUCATION')

        data = dataToMerge.groupby('YEAR').EDUCATION.apply(pd.value_counts)
        res = pd.DataFrame(columns=['x', 'y', 'group'])
        index = 0
        for x, value in data.iteritems():
            res.loc[index] = [x[0], value, x[1]]
            index = index + 1

        data = res
        dataGroup = group
        dataX = dataToMerge.YEAR.unique().tolist()

    elif chartname == "1":
        values = dataPWD.groupby('EDUCATION').YEAR.apply(pd.value_counts)
        dataPetition = pd.DataFrame(columns=['education', 'year', 'value'])
        index = 0
        for x, value in values.iteritems():
            dataPetition.loc[index] = [x[0], x[1], value]
            index = index + 1
        data = dataPetition
        dataGroup = ct.EDUCATION;

    chart_data = data.to_dict(orient='records')
    chart_data = json.dumps(chart_data, indent=2)
    group_data = json.dumps(dataGroup, indent=2)
    x_data = json.dumps(dataX, indent=2)
    data = {'chart_data': chart_data}
    data['group_data'] = group_data
    data['x_data'] = x_data
    return render_template('scatterplot.html', data=data)

@app.route("/test", methods = ['POST', 'GET'])
def test():
    chart_data = {'x': [1, 2], 'y': [3, 4]}
    # chart_data = data.to_dict(orient='records')
    chart_data = json.dumps(chart_data, indent=2)
    data = {'chart_data': chart_data}
    return render_template('test.html', data=data)

@app.route("/test2/<string:dataset>", methods = ['POST', 'GET'])
def test2(dataset):

    #gridmap: gm
    gm_category = "none"
    gm_categories = []
    gm_categoryName = "none"

    gm_dataset = "Mean Wage"
    gm_groups = (dataH1B.groupby('STATE').mean().WAGE).round(2)
    gm_data = json.dumps(gm_groups.to_dict(), indent=2)
    gm_dataDomain = [0, 375000, 750000, 1125000, 1500000]

    data = {'gm_chart_data': gm_data}
    data['gm_dataname'] = "'" + gm_dataset + "'"
    data['gm_states'] = ct.STATES
    data['gm_domain'] = gm_dataDomain
    data['gm_category'] = "'" + gm_category + "'"
    data['gm_categories'] = gm_categories
    data['gm_categoryname'] = "'" + gm_categoryName + "'"

    #scatterplot: sp
    sp_removeCategory = [1,2,3,4]
    sp_dataToMerge, sp_group = mergeOther(dataH1B.copy(), ct.STATUS_H1B, sp_removeCategory, 'STATUS')
    sp_data = sp_dataToMerge.groupby('YEAR').STATUS.apply(pd.value_counts)
    sp_res = pd.DataFrame(columns=['x', 'y', 'group'])
    sp_index = 0
    for sp_x, sp_value in sp_data.iteritems():
        sp_res.loc[sp_index] = [sp_x[0], sp_value, sp_x[1]]
        sp_index = sp_index + 1
    sp_data = sp_res
    sp_dataGroup = sp_group
    sp_dataX = sp_dataToMerge.YEAR.unique().tolist()

    sp_chart_data = sp_data.to_dict(orient='records')
    sp_chart_data = json.dumps(sp_chart_data, indent=2)
    sp_group_data = json.dumps(sp_dataGroup, indent=2)
    sp_x_data = json.dumps(sp_dataX, indent=2)

    data['sp_chart_data'] = sp_chart_data
    data['sp_group_data'] = sp_group_data
    data['sp_x_data'] = sp_x_data

    return render_template('test2.html', data=data)

# data[Y].[:N] will get the top n companies in year Y
def getEmployerPartition(data):
    return data.groupby(['YEAR']).EMPLOYER.apply(pd.value_counts)

def getEmployerPartitionForYear(data, num):
    res = []
    for year in ct.YEARS:
        dfYear = data[year][:num].to_frame().rename(columns={'EMPLOYER': 'PETITION'})
        dfYear['EMPLOYER'] = dfYear.index
        dfYear['EMPLOYER'] = dfYear['EMPLOYER'].apply(
            lambda x: string.capwords(x))
        dfYear['YEAR'] = year
        res.append(dfYear)
    res = pd.concat(res)
    return res

if __name__ == "app":
    dataH1B = pd.read_csv('/Users/hang/PycharmProjects/EmploymentOfForeignersVisualization/data/H-1B_numeric.csv', low_memory=False)
    dataPWD = pd.read_csv('/Users/hang/PycharmProjects/EmploymentOfForeignersVisualization/data/PWD_numeric.csv', low_memory=False)
    dataPERM = pd.read_csv('/Users/hang/PycharmProjects/EmploymentOfForeignersVisualization/data/PERM_numeric.csv', low_memory=False)
    dataEmployerPartition = getEmployerPartition(dataH1B)
    app.run(debug=True)
