#!/usr/bin/env python
# -*- coding: utf-8 -*-
# code for python3

import cv2
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def moving_average(x, y):
    y_conv = np.convolve(y, np.ones(5)/float(5), mode='valid')
    x_dat = np.linspace(np.min(x), np.max(x), np.size(y_conv))
    return x_dat, y_conv


print("start analyze!")

# get movie
cap1 = cv2.VideoCapture("mov/mov01.avi")
cap2 = cv2.VideoCapture("mov/mov02.avi")
width1 = cap1.get(cv2.CAP_PROP_FRAME_WIDTH)
height1 = cap1.get(cv2.CAP_PROP_FRAME_HEIGHT)
width2 = cap2.get(cv2.CAP_PROP_FRAME_WIDTH)
height2 = cap2.get(cv2.CAP_PROP_FRAME_HEIGHT)
# count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
fps1 = cap1.get(cv2.CAP_PROP_FPS)
fps2 = cap2.get(cv2.CAP_PROP_FPS)
# print("image width : " + str(width))
# print("image height : " + str(height))
# print("the num of frames : " + str(count))
# print("frame rate(fps) : " + str(fps))


# declare HOG
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
hogParams = {'winStride': (8, 8), 'padding': (
    32, 32), 'scale': 1.05, 'hitThreshold': 0, 'finalThreshold': 5}


# output
num1 = 0
num2 = 0
list_df1 = pd.DataFrame(columns=['time', 'people'])
list_df2 = pd.DataFrame(columns=['time', 'people'])


while(cap1.isOpened()):
    ret1, frame1 = cap1.read()
    if ret1:
        if(num1 % 10 == 0):
            gray1 = cv2.cvtColor(frame1, cv2.COLOR_RGB2GRAY)
            human1, r1 = hog.detectMultiScale(gray1, **hogParams)
            if (len(human1) > 0):
                for (x1, y1, w1, h1) in human1:
                    cv2.rectangle(frame1, (x1, y1), (x1 + w1, y1 + h1),
                                  (255, 255, 255), 3)
            tmp_se1 = pd.Series([num1/fps1, len(human1)],
                                index=list_df1.columns)
            list_df1 = list_df1.append(tmp_se1, ignore_index=True)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    else:
        break
    num1 = num1 + 1

while(cap2.isOpened()):
    ret2, frame2 = cap2.read()
    if ret2:
        if(num2 % 10 == 0):
            gray2 = cv2.cvtColor(frame2, cv2.COLOR_RGB2GRAY)
            human2, r2 = hog.detectMultiScale(gray2, **hogParams)
            if (len(human2) > 0):
                for (x2, y2, w2, h2) in human2:
                    cv2.rectangle(frame2, (x2, y2), (x2 + w2, y2 + h2),
                                  (255, 255, 255), 3)
            tmp_se2 = pd.Series([num2/fps2, len(human2)],
                                index=list_df2.columns)
            list_df2 = list_df2.append(tmp_se2, ignore_index=True)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    else:
        break
    num2 = num2 + 1

cap1.release()
cap2.release()
cv2.destroyAllWindows()
print("finished analysing!")

# plt.plot(list_df1["time"], list_df1["people"], label="test1")
ma_x1, ma_y1 = moving_average(list_df1["time"], list_df1["people"])
# plt.plot(ma_x1, ma_y1, label="average")
# plt.xlabel('time(sec')
# plt.ylabel('population')
# plt.ylim(0, 15)

# plt.plot(list_df2["time"], list_df2["people"], label="test2")
ma_x2, ma_y2 = moving_average(list_df2["time"], list_df2["people"])
# plt.plot(ma_x2, ma_y2, label="average")
# plt.xlabel('time(sec')
# plt.ylabel('population')
# plt.ylim(0, 15)

plt.plot(ma_x1, ma_y1, label="1st")
plt.plot(ma_x2, ma_y2, label="2nd")
plt.xlabel('time(sec')
plt.ylabel('population')
plt.ylim(0, 15)
plt.legend()
plt.show()