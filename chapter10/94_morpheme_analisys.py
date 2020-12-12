#!/usr/bin/env python
# -*- coding: utf-8 -*-
# code for python3

import pandas as pd
import matplotlib.pyplot as plt
import MeCab

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
# print(survey["comment"].head())
# print()

survey["comment"] = survey["comment"].str.replace("\(.+?\)", "", regex=True)
# print(survey["comment"].head())
# print()

survey["comment"] = survey["comment"].str.replace("\（.+?\）", "", regex=True)
# print(survey["comment"].head())
# print()

survey["length"] = survey["comment"].str.len()
# print(survey.head())
# plt.hist(survey["length"])
# plt.show()

tagger = MeCab.Tagger()
text = "すもももももももものうち"
words = tagger.parse(text).splitlines()
words_arr = []
for i in words:
    if i == 'EOS':
        continue
    word_tmp = i.split()[0]
    words_arr.append(word_tmp)
print(words_arr)