#!/usr/bin/env python
# -*- coding: utf-8 -*-
# code for python3

import pandas as pd

# load data
sales_data = pd.read_csv("uriage.csv")
# print(sales_data.head())
# print()
customer_data = pd.read_excel("kokyaku_daicho.xlsx")
# print(customer_data.head())

# check inconsistency in spelling or wording
print(sales_data["item_name"].head())
print(sales_data["item_price"].head())