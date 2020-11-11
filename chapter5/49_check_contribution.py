#!/usr/bin/env python
# -*- coding: utf-8 -*-
# code for python3

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn import linear_model
from sklearn.tree import DecisionTreeClassifier
import sklearn.model_selection
import sklearn.model_selection
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt

# set the MAX num of rows and columns that will be displayed at terminal
pd.set_option('display.max_rows', 100000)
pd.set_option('display.max_columns', 100)

# load data
customer = pd.read_csv('customer_join.csv')
uselog_months = pd.read_csv('use_log_months.csv')

# data processing for machine learning
# refer 36_~~.py in chapter4
year_months = list(uselog_months["年月"].unique()) # make list of months from Apr to Mar
# print(year_months)
uselog = pd.DataFrame() # prepare empty data
for i in range (1, len(year_months)): # from May-2018 to Mar-2019, since we're going to use last & current month's data to predict next month
    tmp = uselog_months.loc[uselog_months["年月"]==year_months[i]]
    tmp.rename(columns={"count":"count_0"}, inplace=True)
    tmp_before = uselog_months.loc[uselog_months["年月"]==year_months[i-1]]
    del tmp_before["年月"]
    tmp_before.rename(columns={"count":"count_1"}, inplace=True)
    tmp = pd.merge(tmp, tmp_before, on="customer_id", how="left")
    uselog = pd.concat([uselog, tmp], ignore_index=True)
# print(uselog.head())

# add new column for months when exited customers submitted form to exit membership
# since if you want to predict someone's exit, you have to survey months when customers
# submitted forms or earlier months
exit_customer = customer.loc[customer["is_deleted"]==1] # extract exited customers
exit_customer["exit_date"] = None # add new columns
exit_customer["end_date"] = pd.to_datetime(exit_customer["end_date"]) # reformat date data
for i in range(len(exit_customer)):  # for all exited customers, ///
    # add month data for single months before from end date
    exit_customer["exit_date"].iloc[i] = exit_customer["end_date"].iloc[i] - relativedelta(months=1)
exit_customer["exit_date"] = pd.to_datetime(exit_customer["exit_date"]) # reformat date data(not in textbook, but necessary)
exit_customer["年月"] = exit_customer["exit_date"].dt.strftime("%Y%m") # reform to YYYYmm style
uselog["年月"] = uselog["年月"].astype(str) # reformat as string type
exit_uselog = pd.merge(uselog, exit_customer, on=["customer_id", "年月"], how="left") # merge to use log data
# print(len(uselog)) # this data is based on uselog, so the num of articles are as many as 33851
# print(exit_uselog.head()) # but still many of 33851 articles are NaN because main part of data is for exitted customers
exit_uselog = exit_uselog.dropna(subset=["name"]) # remove data include NaN, since it means those customers still in our membership
# print(len(exit_uselog))
# print(len(exit_uselog["customer_id"].unique()))
# print(exit_uselog.head())


conti_customer = customer.loc[customer["is_deleted"] == 0] # extract customers' data still continuing membership
conti_uselog = pd.merge(uselog, conti_customer, on=["customer_id"], how="left") # merge to uselog
# print(len(conti_uselog)) # the num of all articles in the data
conti_uselog = conti_uselog.dropna(subset=["name"]) # delete articles which "name" is NaN(it means the user of the article already exit membership)
# print(len(conti_uselog))

# execute downsampling since the num of articles of conti_users are far more larger than exit users
conti_uselog = conti_uselog.sample(frac=1).reset_index(drop=True) # shuffle the order of the articles
conti_uselog = conti_uselog.drop_duplicates(subset="customer_id") # delete all data other than the 1st article for each customers
# print(len(conti_uselog))
# print(conti_uselog.head())

# unify exit customers' data and continue customers' data
predict_data = pd.concat([conti_uselog, exit_uselog], ignore_index=True)
# print(len(predict_data))
# print(predict_data.head())

# add parameters for length of membership term
# refer also 37_~~.py, but it's still different from those "membership period"
# because in those case, "membership period" means periods last to end of Mar-2019,
# and in this case, "period" means it last to each day of use log.
predict_data["period"] = 0
predict_data["now_date"] = pd.to_datetime(predict_data["年月"], format="%Y%m")
predict_data["start_date"] = pd.to_datetime(predict_data["start_date"])
for i in range(len(predict_data)):
    delta = relativedelta(predict_data["now_date"][i], predict_data["start_date"][i])
    predict_data["period"][i] = int(delta.years*12 + delta.months)
# print(predict_data.head())


# check missed data
# there're missed data in "end_date", "exit_date", "count_1", and former 2 data are only for exitted customers
# if count_1 is zero, it means it's his/her 1st months of their membership
# print(predict_data.isna().sum())
predict_data = predict_data.dropna(subset=["count_1"])
# print(predict_data.isna().sum())
print()

# reformat data into dummy parameters
# first, extract data only might be related.
target_col = ["campaign_name", "class_name", "gender", "count_1", "routine_flg", "period", "is_deleted"]
predict_data = predict_data[target_col]
# print(predict_data.head())

# change category data into flag data (i.e. if a customer's sex is male,
# currently the data says column "gender" is "M". but for ML, string data "M" is not suitable,
# so change it into flag data : e.g. is_male = true )
predict_data = pd.get_dummies(predict_data)
# print(predict_data.head())

# delete duplicated data
# i.e. if flag "is_male" is true, you don't have to say "is_female" is false
del predict_data["campaign_name_通常"]
del predict_data["class_name_ナイト"]
del predict_data["gender_M"]
# print(predict_data.head())


exit = predict_data.loc[predict_data["is_deleted"]==1]
conti = predict_data.loc[predict_data["is_deleted"]==0].sample(len(exit)) # unify the num of articles to data for exit
X = pd.concat([exit, conti], ignore_index = True)
y = X["is_deleted"]
del X["is_deleted"]
X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(X, y)
model = DecisionTreeClassifier(random_state=0)
model.fit(X_train, y_train)
y_test_pred = model.predict(X_test)
# print(y_test_pred)
# compare actual data and predicted results
results_test = pd.DataFrame({"y_test":y_test, "y_pred":y_test_pred })
# print(results_test.head())

# check the correct ratio of the last prediction model above
correct = len(results_test.loc[results_test["y_test"]==results_test["y_pred"]])
data_count = len(results_test)
score_test = correct/data_count
# print(score_test)

# check the correct ratio of both train data and test data
# correct ratio for train data are 10 points higher than test data i.e. over fitting a bit
print(model.score(X_test, y_test))
print(model.score(X_train, y_train))
print('---------clearing overfitting------------')

# improve model to clear current state : overfitting
# for this purpose, make depth of the decision tree more shallow
model = DecisionTreeClassifier(random_state=0, max_depth=5) # set maximum depth to 5 (as default, it is set as none that means infinite)
model.fit(X_train, y_train)
print(model.score(X_test, y_test))
print(model.score(X_train, y_train))

# check contribution from each parameters
# refer also 39_~~.py
importance = pd.DataFrame({"feature_names": X.columns, "coefficient": model.feature_importances_ })
print()
print(importance)
