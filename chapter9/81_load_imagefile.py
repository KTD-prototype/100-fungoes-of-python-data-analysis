#!/usr/bin/env python
# -*- coding: utf-8 -*-
# code for python3

import cv2
img = cv2.imread("img/img01.jpg")
height, width = img.shape[:2]
print("image width : " + str(width))
print("image height : " + str(height))
cv2.imshow("img", img)
cv2.waitKey(0)