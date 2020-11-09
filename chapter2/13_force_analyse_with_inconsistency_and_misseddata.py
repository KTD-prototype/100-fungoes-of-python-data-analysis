#!/usr/bin/env python
# -*- coding: utf-8 -*-
# code for python3

import pandas as pd

# set the MAX num of columns that will be displayed at terminal
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

# ignore data inconsistency in spelling or wording and data missing
sales_data["purchase_date"]=pd.to_datetime(sales_data["purchase_date"])
sales_data["purchase_month"]=sales_data["purchase_date"].dt.strftime("%Y%m")
# res = sales_data.pivot_table(index="purchase_month", columns="item_name", aggfunc="size", fill_value=0)
res = sales_data.pivot_table(index="purchase_month", columns="item_name", values="item_price", aggfunc="sum", fill_value=0)
print(res)