#!/usr/bin/env python
# -*- coding: utf-8 -*-
# code for python3

import cv2

print("start saving your timelapse video!")


# get info
cap = cv2.VideoCapture("mov/mov01.avi")
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


# generate timelapse
movie_name = "timelapse.avi"
fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
apiReference_param = 1
# set configuration of video output.
# you have to set parameters as integer value (otherwise you are asked to set another parameter 'apiReference', which I can't figure out what it means)
video = cv2.VideoWriter(movie_name, fourcc, int(fps),
                        (int(width), int(height)), True)


# output
num = 0
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
            video.write(frame)
    else:
        break
    num = num + 1
video.release()
cap.release()
cv2.destroyAllWindows()
print("your timelapse has been saved!")
