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

# load data
customer = pd.read_csv('customer_join.csv')
uselog_months = pd.read_csv('use_log_months.csv')

# data processing for machine learning
# refer 36_~~.py in chapter4
year_months = list(uselog_months["年月"].unique()) # make list of months from Apr to Mar
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
print(len(uselog)) # this data is based on uselog, so the num of articles are as many as 33851
# print(exit_uselog.head()) # but still many of 33851 articles are NaN because main part of data is for exitted customers
exit_uselog = exit_uselog.dropna(subset=["name"]) # remove data include NaN, since it means those customers still in our membership
print(len(exit_uselog))
print(len(exit_uselog["customer_id"].unique()))
print(exit_uselog.head())
