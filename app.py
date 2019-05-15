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
            nEmployerPartition= 10
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

@app.route("/gridmap", methods = ['POST', 'GET'])
def gridmap():
    chart_data = {'x': [1, 2], 'y': [3, 4]}
    # chart_data = data.to_dict(orient='records')
    chart_data = json.dumps(chart_data, indent=2)
    data = {'chart_data': chart_data}
    return render_template('gridmap.html', data=data)

@app.route("/heatmap", methods = ['POST', 'GET'])
def heatmap():
    data = dataH1B.corr()

    dataHeatmap = pd.DataFrame(columns=['x', 'y', 'value'])

    index = 0
    for x, values in data.iteritems():
        for y, value in values.iteritems():
            dataHeatmap.loc[index] = [x, y, value]
            index = index + 1

    chart_data = dataHeatmap.to_dict(orient='records')
    chart_data = json.dumps(chart_data, indent=2)
    data = {'chart_data': chart_data}
    return render_template('heatmap.html', data=data)

@app.route("/barchart", methods = ['POST', 'GET'])
def barchart():
    data = dataH1B.groupby(['STATE']).size().to_frame("y")
    data["x"] = data.index
    chart_data = data.to_dict(orient='records')
    chart_data = json.dumps(chart_data, indent=2)
    data = {'chart_data': chart_data}
    return render_template('barchart.html', data=data)

@app.route("/test", methods = ['POST', 'GET'])
def test():
    chart_data = {'x': [1, 2], 'y': [3, 4]}
    # chart_data = data.to_dict(orient='records')
    chart_data = json.dumps(chart_data, indent=2)
    data = {'chart_data': chart_data}
    return render_template('test.html', data=data)

# def getScatterMDS(data):
#     dataframe = applyMDS(data, 2)
#     res = dataframe.rename(columns={'mds-1':'x', 'mds-2': 'y'})
#     print("plot for MDS")
#     print(res)
#     return res
#
# def getScatterPCA(data):
#     dataframe = applyPCA(data, 2)
#     res = dataframe.rename(columns={'pc-1':'x', 'pc-2': 'y'})
#     print("plot for PCA")
#     print(res)
#     return res
#
# def applyMDS(data, n_components):
#     nCol = len(data.columns)
#     # data = scale(data)
#     res = MDS(n_components=n_components).fit_transform(data)
#     # print("in applyMDS:", res)
#     columns = ['mds-' + str(i) for i in range(1, n_components+1)]
#     res = pd.DataFrame(data = res, columns =columns)
#     return res
#
# def applyPCA(data, n_components):
#     nCol = len(data.columns)
#     # data = scale(data)
#     res = PCA(n_components=n_components).fit_transform(data)
#     # print("in applyPCA:", res)
#     columns = ['pc-' + str(i) for i in range(1, n_components+1)]
#     res = pd.DataFrame(data = res, columns =columns)
#     return res
#
# def getPCAScree(data):
#     # @ x: number of omponents
#     # @ y: ratio of variance explained
#     # @ explained_variance_ratio_
#     #     Percentage of variance explained by each of the selected components
#     nCol = len(data.columns)
#     # data = scale(data)
#     xVals = [i for i in range(1, nCol + 1)]
#     yVals = PCA(n_components=nCol).fit(data).explained_variance_ratio_
#     # print("estimated n_com:", PCA(n_components=nCol).fit(data).components_)
#
#     for i in range(1, len(yVals)):
#         yVals[i] += yVals[i-1]
#     dataframe = pd.DataFrame({'x':xVals, 'y': yVals})
#     return dataframe
#
# def getElbow(data):
#     # @ x: number of clusters
#     # @ y: sum of squared distances
#     # @ Objective - Minimize squared error
#     #     J = \sum_{j=1}^{k}\sum_{i=1}^{n} (||x_{i}^{j}-c_{j}||)^2
#     #     @ k: # clusters
#     #     @ n: # cases
#     #     @ x: case
#     #     @ c: centroid for cluster
#     # @ inertia_: float
#     #     Kmeans Attribute
#     #     Sum of squared distances of samples to their cloest cluster center.
#     xVals = []
#     yVals = []
#     for i in range(2, 12):
#         xVals.append(i)
#         yVals.append(KMeans(n_clusters = i).fit(data).inertia_)
#     dataframe = pd.DataFrame({'x':xVals, 'y': yVals})
#     return dataframe

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
    dataH1B = pd.read_csv(ct.PATH_H1B + "numeric" + ct.EXT_TO, low_memory=False)
    dataEmployerPartition = getEmployerPartition(dataH1B)
    app.run(debug=True)
