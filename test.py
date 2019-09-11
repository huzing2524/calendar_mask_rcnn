# -*- coding: utf-8 -*-
# @Time   : 19-8-7 上午10:14
# @Author : huziying
# @File   : test.py

import cv2
import skimage
import numpy

image = cv2.imread('/home/dsd/Desktop/calendar_mask_rcnn/dataset/train/sample.png')

print(image.shape)  # (318, 606, 3)
'''
>>> img = np.zeros((5, 5), dtype=np.uint8)
>>> start = (0, 1)
>>> end = (3, 3)
>>> rr, cc = rectangle(start, end=end, shape=img.shape)
>>> img[rr, cc] = 1
>>> img
array([[0, 1, 1, 1, 0],
       [0, 1, 1, 1, 0],
       [0, 1, 1, 1, 0],
       [0, 1, 1, 1, 0],
       [0, 0, 0, 0, 0]], dtype=uint8)
'''
img = numpy.zeros((318, 606, 3), dtype=numpy.uint8)
start = (32, 401)
end = (32 + 37, 401 + 32)
rr, cc = skimage.draw.rectangle(start, end)
img[rr, cc] = 0
# print(rr, cc)

cv2.rectangle(image, (401, 32), (401 + 32, 32 + 37), (255, 0, 255), 2)

cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.imshow('image', image)
cv2.waitKey(0)

cv2.namedWindow('img', cv2.WINDOW_NORMAL)
cv2.imshow('img', img)
cv2.waitKey(0)

cv2.destroyAllWindows()
