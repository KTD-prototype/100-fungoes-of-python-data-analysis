#!/usr/bin/env python
# -*- coding: utf-8 -*-
# code for python3

import pandas as pd

# set the MAX num of rows and columns that will be displayed at terminal
pd.set_option('display.max_rows', 100000)
pd.set_option('display.max_columns', 100)

# load the file
sales_data = pd.read_csv("uriage.csv")
customer_data = pd.read_excel("kokyaku_daicho.xlsx")
import_data = pd.read_csv("dump_data.csv")
# print(import_data.head())


# clean data (following codes are copied from lesson 11-19)
sales_data["purchase_date"] = pd.to_datetime(sales_data["purchase_date"])
sales_data["purchase_month"] = sales_data["purchase_date"].dt.strftime("%Y%m")
# replace lower case letter with capitals
sales_data["item_name"] = sales_data["item_name"].str.upper()
sales_data["item_name"] = sales_data["item_name"].str.replace(
    "　", "")  # replace space from the data of item names
sales_data["item_name"] = sales_data["item_name"].str.replace(
    " ", "")  # replace space from the data of item names
# replace NULL data you've found in column "price" with correct value
# you can replace them because you have constant price for each items
flg_is_null = sales_data["item_price"].isnull()
# print(flg_is_null)
for trg in list(sales_data.loc[flg_is_null, "item_name"].unique()):
    price = sales_data.loc[(~flg_is_null) & (
        sales_data["item_name"] == trg), "item_price"].max()
    sales_data["item_price"].loc[(flg_is_null) & (
        sales_data["item_name"] == trg)] = price
# correct inconsistency of spelling for customer data
customer_data["顧客名"] = customer_data["顧客名"].str.replace("　", "")
customer_data["顧客名"] = customer_data["顧客名"].str.replace(" ", "")
# unify the format of date data
flg_is_serial = customer_data["登録日"].astype(
    "str").str.isdigit()  # whether the date data format is digit
fromSerial = pd.to_timedelta(customer_data.loc[flg_is_serial, "登録日"].astype(
    "float"), unit="D") + pd.to_datetime("1900/01/01")
fromString = pd.to_datetime(customer_data.loc[~flg_is_serial, "登録日"])
customer_data["登録日"] = pd.concat([fromSerial, fromString])


# count how many items were selled based on purchase month
byItem = import_data.pivot_table(
    index="purchase_month", columns="item_name", aggfunc="size", fill_value=0)
# print(byItem)

# count how much sales have been earned based on purchase month
byPrice = import_data.pivot_table(
    index="purchase_month", columns="item_name", values="item_price", aggfunc="sum", fill_value=0)
# print(byPrice)

# count who has been bought based on purchase month
byCustomer = import_data.pivot_table(
    index="purchase_month", columns="顧客名", aggfunc="size", fill_value=0)
# print(byCustomer)

# count where the purchases was done based on purchase month
byRegion = import_data.pivot_table(
    index="purchase_month", columns="地域", aggfunc="size", fill_value=0)
# print(byRegion)

# check whether there're customers who didn't by anything
away_data = pd.merge(sales_data, customer_data,
                     left_on="customer_name", right_on="顧客名", how="right")
# print(customer_data)
# print(sales_data)
# print(away_data)
print(away_data.head())
print(away_data[away_data["purchase_date"].isnull()]
      [["顧客名", "メールアドレス", "登録日"]])
