#!/usr/bin/env python
# -*- coding: utf-8 -*-
# code for python3
import pandas as pd
import matplotlib.pyplot as plt


# set the MAX num of columns that will be displayed at terminal
pd.set_option('display.max_columns', 100)

customer_master = pd.read_csv('customer_master.csv')
# print(customer_master.head())
# print()

item_master = pd.read_csv('item_master.csv')
# print(item_master.head())
# print()

transaction_1 = pd.read_csv('transaction_1.csv')
transaction_2 = pd.read_csv('transaction_2.csv')
transaction = pd.concat([transaction_1, transaction_2], ignore_index=True)
# print(transaction.head())
# print()
# print(len(transaction_1))
# print(len(transaction_2))
# print(len(transaction))
# print()

transaction_detail_1 = pd.read_csv('transaction_detail_1.csv')
transaction_detail_2 = pd.read_csv('transaction_detail_2.csv')
transaction_detail = pd.concat(
    [transaction_detail_1, transaction_detail_2], ignore_index=True)
# print(transaction_detail.head())
# print()
# print(len(transaction_detail_1))
# print(len(transaction_detail_2))
# print(len(transaction_detail))
# print()

# merge "transaction" to "transaction__detail" for merge data on payment_date & customer_id based on common data "transaction_id"
join_data = pd.merge(transaction_detail, transaction[[
                     "transaction_id", "payment_date", "customer_id"]], on="transaction_id", how="left")
# print(join_data.head())  # check first 5 lines of the data

# check the num of lines of the data
# print(len(transaction_detail))
# print(len(transaction))
# print(len(join_data))

# merge customer data & item data to joined transaction data, based on "customer_id" and "item_id" for each.
join_data = pd.merge(join_data, customer_master, on="customer_id", how="left")
join_data = pd.merge(join_data, item_master, on="item_id", how="left")
# print(join_data.head())

# add total price of each transactions
join_data["price"] = join_data["quantity"]*join_data["item_price"]
# print(join_data[["quantity", "item_price", "price"]].head())

# # check data by checking sumention of the price of all transactions
# print(join_data["price"].sum())
# print(transaction["price"].sum())

# # check the num of data that is missed
# print(join_data.isnull().sum())

# # display some kinds of statistical data
# print(join_data.describe())
# print()
# print(join_data["payment_date"].min())
# print(join_data["payment_date"].max())

# # check data type
# print(join_data.dtypes)

# convert data-type of "payment_date" from object to datetime and add new column of payment months
join_data["payment_date"] = pd.to_datetime(join_data["payment_date"])
join_data["payment_month"] = join_data["payment_date"].dt.strftime("%Y%m")
# print(join_data[["payment_date", "payment_month"]].head())

# # export join_data as CSV file
# join_data.to_csv("join_data.csv")

# # group data by month and sum it
# grouped_data = join_data.groupby("payment_month").sum()["price"]
# print(grouped_data)

# # display sum of sell and quantity of them sorted by months and items
# grouped_data_2 = join_data.groupby(["payment_month", "item_name"]).sum()[
#     ["price", "quantity"]]
# # grouped_data_2 = join_data.groupby(["item_name", "payment_month"]).sum()[["price", "quantity"]]
# print(grouped_data_2)

# # change way to display by pivot table
# pivottted_data = pd.pivot_table(join_data, index='item_name', columns='payment_month', values=[
#                                 'price', 'quantity'], aggfunc='sum')
# print(pivottted_data)

# visualize data after arrange data by pivot data
graph_data = pd.pivot_table(join_data, index='payment_month',
                            columns='item_name', values='price', aggfunc='sum')
# print(graph_data)
plt.plot(list(graph_data.index), graph_data["PC-A"], label='PC-A')
plt.plot(list(graph_data.index), graph_data["PC-B"], label='PC-B')
plt.plot(list(graph_data.index), graph_data["PC-C"], label='PC-C')
plt.plot(list(graph_data.index), graph_data["PC-D"], label='PC-D')
plt.plot(list(graph_data.index), graph_data["PC-E"], label='PC-E')
plt.legend()
plt.show()