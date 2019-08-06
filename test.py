# -*- coding: utf-8 -*-
# @Time   : 19-8-6 下午5:26
# @Author : huziying
# @File   : test.py

import cv2
"""
坐标 x1, y1, x2, y2
opencv裁剪图片: img[y1:y2, x1:y1] 坐标系可能是相反的"""

img = cv2.imread('/home/dsd/Desktop/calendar_faster_rcnn/dataset/train/sample.png')
cv2.imshow('img', img[89:127, 142:174])
cv2.waitKey(0)
cv2.destroyAllWindows()
