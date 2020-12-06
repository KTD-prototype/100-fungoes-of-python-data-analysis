#!/usr/bin/env python
# -*- coding: utf-8 -*-
# code for python3

import cv2
import pandas as pd
import matplotlib.pyplot as plt

print("start analyze!")

# get movie
cap = cv2.VideoCapture("mov/mov02.avi")
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
# count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
fps = cap.get(cv2.CAP_PROP_FPS)
print("image width : " + str(width))
print("image height : " + str(height))
# print("the num of frames : " + str(count))
# print("frame rate(fps) : " + str(fps))


# declare HOG
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
hogParams = {'winStride': (8, 8), 'padding': (
    32, 32), 'scale': 1.05, 'hitThreshold': 0, 'finalThreshold': 5}


# output
num = 0
list_df = pd.DataFrame(columns=['time', 'people'])
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret:
        if(num % 10 == 0):
            gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            human, r = hog.detectMultiScale(gray, **hogParams)
            if (len(human) > 0):
                for (x, y, w, h) in human:
                    cv2.rectangle(frame, (x, y), (x + w, y + h),
                                  (255, 255, 255), 3)
            tmp_se = pd.Series([num/fps, len(human)], index=list_df.columns)
            list_df = list_df.append(tmp_se, ignore_index=True)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    else:
        break
    num = num + 1
cap.release()
cv2.destroyAllWindows()
print("finished analysing!")

plt.plot(list_df["time"], list_df["people"], label="test")
plt.xlabel('time(sec')
plt.ylabel('population')
plt.ylim(0, 15)
plt.show()
