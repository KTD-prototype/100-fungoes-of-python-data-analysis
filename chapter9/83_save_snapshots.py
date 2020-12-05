#!/usr/bin/env python
# -*- coding: utf-8 -*-
# code for python3

import cv2


# get info
cap = cv2.VideoCapture("mov/mov01.avi")
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
fps = cap.get(cv2.CAP_PROP_FPS)
print("image width : " + str(width))
print("image height : " + str(height))
print("the num of frames : " + str(count))
print("frame rate(fps) : " + str(fps))


# output
num = 0
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret:
        cv2.imshow("frame", frame)
        filepath = "snapshot/snapshot_" + str(num) + ".jpg"
        cv2.imwrite(filepath, frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    num = num + 1
cap.release()
cv2.destroyAllWindows()