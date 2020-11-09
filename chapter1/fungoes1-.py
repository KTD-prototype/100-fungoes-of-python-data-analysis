#!/usr/bin/env python
# -*- coding: utf-8 -*-
# code for python3
import pandas as pd

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
transaction_detail = pd.concat([transaction_detail_1, transaction_detail_2], ignore_index=True)
# print(transaction_detail.head())
# print()
# print(len(transaction_detail_1))
# print(len(transaction_detail_2))
# print(len(transaction_detail))
# print()
