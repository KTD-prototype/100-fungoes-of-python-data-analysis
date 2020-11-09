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
print(customer_join.head())
print(len(customer))
print(len(customer_join))

# check whether there're missed data
print(customer_join.isnull().sum())