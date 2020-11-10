#!/usr/bin/env python
# -*- coding: utf-8 -*-
# code for python3

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn import linear_model
import sklearn.model_selection
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt

# set the MAX num of rows and columns that will be displayed at terminal
pd.set_option('display.max_rows', 100000)
pd.set_option('display.max_columns', 100)

# load files
uselog = pd.read_csv('../chapter3/use_log.csv')
# print(uselog.isnull().sum())
customer = pd.read_csv('../chapter3/customer_join.csv')
# print(customer.isnull().sum())

# extract data that we need to analyse
customer_clustering = customer[["mean", "median", "max", "min", "membership_period"]]
# print(customer_clustering.head())
sc = StandardScaler()# setup imported library
customer_clustering_sc = sc.fit_transform(customer_clustering) # standerize data
kmeans = KMeans(n_clusters=4, random_state=0) # define a model for clustering
clusters = kmeans.fit(customer_clustering_sc) # set the data to be processed and execute clustering
customer_clustering["cluster"] = clusters.labels_ # merge results to original data
# print(customer_clustering["cluster"].unique())
# print(customer_clustering.head())

# rename labels of the data
customer_clustering.columns = ["月内平均値", "月内中央値", "月内最大値", "月内最小値", "会員期間", "cluster"]
# check the num of each data
customer_clustering.groupby("cluster").count()
# print(customer_clustering.groupby("cluster").count())
# get mean value of each clusters
customer_clustering.groupby("cluster").mean()
# print(customer_clustering.groupby("cluster").mean())

# decrease dimension via principal component analysys
X = customer_clustering_sc # extract standerized data
pca = PCA(n_components=2) # define a model : decrease dimension to 2 by PCA
pca.fit(X) # execute PCA, 1st step
x_pca = pca.transform(X) # execute PCA, 2nd step
pca_df = pd.DataFrame(x_pca) # contain analysed data to new dataframe:pca_df
pca_df["cluster"] = customer_clustering["cluster"] # add clusterized data to new data

# # visualize
# for i in customer_clustering["cluster"].unique():
#     tmp = pca_df.loc[pca_df["cluster"]==i]
#     plt.scatter(tmp[0], tmp[1])
# plt.show()

# compare between clustered data and whether each customers are still in our membership
customer_clustering = pd.concat([customer_clustering, customer], axis = 1)
# analyse clusters by whether those customers are deleted from membership or not
customer_clustering.groupby(["cluster", "is_deleted"], as_index=False).count()[["cluster", "is_deleted", "customer_id"]]
# print(customer_clustering.groupby(["cluster", "is_deleted"], as_index=False).count()[["cluster", "is_deleted", "customer_id"]])
# analyse clusters by whether those customers are using our gym routinely
customer_clustering.groupby(["cluster", "routine_flg"], as_index=False).count()[["cluster", "routine_flg", "customer_id"]]
# print(customer_clustering.groupby(["cluster", "routine_flg"], as_index=False).count()[["cluster", "routine_flg", "customer_id"]])
# print(customer_clustering.head())

# ########################################
# predict next month usage of each customers
# predict usage of next month by past 5 months data
# ########################################
# recount data using uselog (similar to 25_.py)
uselog["usedate"] = pd.to_datetime(uselog["usedate"]) # reformat date data
uselog["年月"] = uselog["usedate"].dt.strftime("%Y%m") # generate YYmm data
uselog_months = uselog.groupby(["年月", "customer_id"], as_index = False).count()
uselog_months.rename(columns={"log_id":"count"}, inplace=True)
del uselog_months["usedate"]
# print(uselog_months.head())

# you can only predict each Oct-2018 to Mar-2019,
# since you need past 5 months from the month you want to predict
year_months = list(uselog_months["年月"].unique()) # list of YYmm data : Apr-2018 to Mar-2019
predict_data = pd.DataFrame()
for i in range(6, len(year_months)): # i : from 6 to 11
    tmp = uselog_months.loc[uselog_months["年月"]==year_months[i]] # extract data that is for Oct(2018) to Mar(2019)
    tmp.rename(columns={"count":"count_pred"}, inplace=True) # the num of arrival for each months
    for j in range(1, 7): # j : from 1 to 6
        tmp_before = uselog_months.loc[uselog_months["年月"]==year_months[i - j]] # extract data that is for 1 to 6 month before from i
        del tmp_before["年月"]
        tmp_before.rename(columns={"count":"count_{}".format(j-1)}, inplace=True)
        tmp = pd.merge(tmp, tmp_before, on="customer_id", how="left")
    predict_data = pd.concat([predict_data, tmp], ignore_index = True)
# print(predict_data.head())

# remove data that is for customers who continued membership shorter than 6 months
predict_data = predict_data.dropna()
predict_data = predict_data.reset_index(drop=True)
# print(predict_data.head())

# add length of membership term as an additional parameter for prediction
predict_data = pd.merge(predict_data, customer[["customer_id", "start_date"]], on="customer_id", how="left")
# print(predict_data.head())
predict_data["now_date"] = pd.to_datetime(predict_data["年月"], format="%Y%m")
predict_data["start_date"] = pd.to_datetime(predict_data["start_date"])
predict_data["period"] = None
for i in range(len(predict_data)):
    delta = relativedelta(predict_data["now_date"][i], predict_data["start_date"][i])
    predict_data["period"][i] = delta.years*12 + delta.months
# print(predict_data.head())

# omit data for customers who joined our membership far away past from now since s/he might in stable routine to use our gym
predict_data = predict_data.loc[predict_data["start_date"]>=pd.to_datetime("20180401")]
model = linear_model.LinearRegression() #initialize model
X = predict_data[["count_0", "count_1", "count_2", "count_3", "count_4", "count_5", "period"]]  # define parameter to use for prediction
y = predict_data["count_pred"]                                                                  # define parameter to be predicted
X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(X, y) # devide to train data and test data, 75% & 25% if not explicitly set
model.fit(X_train, y_train)
# print(model.score(X_train, y_train))
# print(model.score(X_test, y_test))

# export contribution score for each parameters to prediction results
coef = pd.DataFrame({"feature_names":X.columns, "coefficient":model.coef_})
print(coef)


# # export data as csv
# customer_clustering.to_csv("customer_clustering.csv", index=False)
# uselog_months.to_csv("uselog_months.csv", index = False)
