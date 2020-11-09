#!/usr/bin/env python
# -*- coding: utf-8 -*-
# code for python3

import pandas as pd

# set the MAX num of rows and columns that will be displayed at terminal
pd.set_option('display.max_rows', 100000)
pd.set_option('display.max_columns', 100)

# load data
sales_data = pd.read_csv("uriage.csv")
# print(sales_data.head())
# print()
customer_data = pd.read_excel("kokyaku_daicho.xlsx")
# print(customer_data.head())

# # check inconsistency in spelling or wording
# print(sales_data["item_name"].head())
# print(sales_data["item_price"].head())

# # ignore data inconsistency in spelling or wording and data missing
# sales_data["purchase_date"]=pd.to_datetime(sales_data["purchase_date"])
# sales_data["purchase_month"]=sales_data["purchase_date"].dt.strftime("%Y%m")
# # res = sales_data.pivot_table(index="purchase_month", columns="item_name", aggfunc="size", fill_value=0)
# res = sales_data.pivot_table(index="purchase_month", columns="item_name", values="item_price", aggfunc="sum", fill_value=0)
# print(res)

# check the spec of the current data
# # the num of unique(w/o dupe) data of item name
# print(len(pd.unique(sales_data.item_name)))

# replace lower case letter with capitals
sales_data["item_name"] = sales_data["item_name"].str.upper()
sales_data["item_name"] = sales_data["item_name"].str.replace(
    "　", "")  # replace space from the data of item names
sales_data["item_name"] = sales_data["item_name"].str.replace(
    " ", "")  # replace space from the data of item names

# sort data by item name with ascending order
corrected_data = sales_data.sort_values(by=["item_name"], ascending=True)
print(corrected_data)  # print

# check the spec of the corrected data
print(pd.unique(sales_data["item_name"]))
print(len(pd.unique(sales_data["item_name"])))
