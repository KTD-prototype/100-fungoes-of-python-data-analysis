#!/usr/bin/env python
# -*- coding: utf-8 -*-
# code for python3

import pandas as pd

# set the MAX num of rows and columns that will be displayed at terminal
pd.set_option('display.max_rows', 100000)
pd.set_option('display.max_columns', 100)

# load data
uselog = pd.read_csv('use_log.csv')
# print(len(uselog))
# print(uselog.head())
# print()

customer = pd.read_csv('customer_master.csv')
# print(len(customer))
# print(customer.head())
# print()

class_master = pd.read_csv('class_master.csv')
# print(len(class_master))
# print(class_master.head())
# print()

campaign_master = pd.read_csv('campaign_master.csv')
# print(len(campaign_master))
# print(campaign_master.head())
# print()


# merge customer class data & campaign_data to customer data
customer_join = pd.merge(customer, class_master, on="class", how="left")
customer_join = pd.merge(customer_join, campaign_master,
                         on="campaign_id", how="left")
# print(customer_join.head())
# print(len(customer))
# print(len(customer_join))

# # check whether there're missed data
# print(customer_join.isnull().sum())

# count data by several index
print(customer_join.groupby("class_name").count()["customer_id"])
print(customer_join.groupby("campaign_name").count()["customer_id"])
print(customer_join.groupby("gender").count()["customer_id"])
print(customer_join.groupby("is_deleted").count()["customer_id"])

# check the num of customers who joined our gym in JFY2018
customer_join["start_date"] = pd.to_datetime(customer_join["start_date"])
customer_start = customer_join.loc[customer_join["start_date"] > pd.to_datetime(
    "20180401")]
print(len(customer_start))
