#!/usr/bin/env python
# -*- coding: utf-8 -*-
# code for python3

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt

# set the MAX num of rows and columns that will be displayed at terminal
pd.set_option('display.max_rows', 100000)
pd.set_option('display.max_columns', 100)

# load files
uselog = pd.read_csv('../chapter3/use_log.csv')
print(uselog.isnull().sum())
customer = pd.read_csv('../customer_join.csv')
print(customer.isnull().sum())
