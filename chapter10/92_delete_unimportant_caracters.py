#!/usr/bin/env python
# -*- coding: utf-8 -*-
# code for python3

import pandas as pd

survey = pd.read_csv("survey.csv")
print()
# print(len(survey))
# print()
# print(survey.head())
# print()
# print(survey.isnull().sum())

survey = survey.dropna() # remove data which includes N/A in comments
# print(survey.isna().sum())

survey["comment"] = survey["comment"].str.replace("AA", "")
print(survey["comment"].head())
print()

survey["comment"] = survey["comment"].str.replace("\(.+?\)", "", regex=True)
print(survey["comment"].head())
print()

survey["comment"] = survey["comment"].str.replace("\（.+?\）", "", regex=True)
print(survey["comment"].head())
print()
