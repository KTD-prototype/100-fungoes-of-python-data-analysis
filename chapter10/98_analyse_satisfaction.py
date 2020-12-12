#!/usr/bin/env python
# -*- coding: utf-8 -*-
# code for python3

import pandas as pd
import matplotlib.pyplot as plt
import MeCab

# set the MAX num of rows and columns that will be displayed at terminal
pd.set_option('display.max_rows', 100000)
pd.set_option('display.max_columns', 100)

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
# text = "すもももももももものうち"
# words = tagger.parse(text).splitlines()
# # print(words)
# words_arr = []
# parts = ["名詞", "動詞"]
# for i in words:
#     if i == 'EOS' or i == '':
#         continue
#     word_tmp = i.split()[0]
#     part = i.split()[4].split("-")[0] # textbook is wrong
#     print(i)
#     print(word_tmp)
#     print(part)
#     if not(part in parts):
#         continue
#     words_arr.append(word_tmp)
# # print(words_arr)

# all_words = []
# parts = ["名詞"]
# j = 0
# for n in range(len(survey)):
#     text = survey["comment"].iloc[n]
#     words = tagger.parse(text).splitlines()
#     # print(words)
#     words_arr = []
#     for i in words:
#         if i == "EOS" or i == "":
#             continue
#         word_tmp = i.split()[0]
#         # print(word_tmp)
#         # print(i)
#         if len(i.split()) > 3:
#             part = i.split()[4].split("-")[0]
#         else:
#             part = i.split()[2].split("-")[0]
#         # print(j)
#         # print(i.split()[4])
#         # print(part)
#         if not (part in parts):
#             continue
#         words_arr.append(word_tmp)
#     all_words.extend(words_arr)
#     j = j + 1
# # print(all_words)

# all_words_df = pd.DataFrame({"words":all_words, "count":len(all_words)*[1]})
# # print(all_words_df.head())
# all_words_df = all_words_df.groupby("words").sum()
# all_words_df.sort_values("count", ascending=False).head()

stop_words = ["の"]
all_words = []
parts = ["名詞"]
satisfaction = []
for n in range(len(survey)):
    text = survey["comment"].iloc[n]
    words = tagger.parse(text).splitlines()
    words_arr = []
    for i in words:
        if i == "EOS" or i == "":
            continue
        word_tmp = i.split()[0]
        if len(i.split()) > 3:
            part = i.split()[4].split("-")[0]
        else:
            part = i.split()[2].split("-")[0]
        if not(part in parts):
            continue
        if word_tmp in stop_words:
            continue
        words_arr.append(word_tmp)
        satisfaction.append(survey["satisfaction"].iloc[n])
    all_words.extend(words_arr)
# print(all_words)

all_words_df = pd.DataFrame({"words":all_words, "satisfaction":satisfaction, "count":len(all_words)*[1]})
print(all_words_df.head())
# all_words_df = all_words_df.groupby("words").sum()
# print(all_words_df.sort_values("count", ascending=False))

words_satisfaction = all_words_df.groupby("words").mean()["satisfaction"]
words_count = all_words_df.groupby("words").sum()["count"]
words_df = pd.concat([words_satisfaction, words_count], axis = 1)
print(words_df)

words_df = words_df.loc[words_df["count"] >= 3]
print(words_df.sort_values("satisfaction", ascending = False).head())
print(words_df.sort_values("satisfaction").head())
