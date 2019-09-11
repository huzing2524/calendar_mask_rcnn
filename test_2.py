# -*- coding: utf-8 -*-
# @Time   : 19-9-11 上午11:11
# @Author : huziying
# @File   : test_2.py

from skimage.color import rgba2rgb
from skimage import data
import skimage
import cv2

image = skimage.io.imread('/home/dsd/Desktop/calendar_mask_rcnn/dataset/train/sample.jpg')
print(image.shape)
# print(image)

image_2 = cv2.imread('/home/dsd/Desktop/calendar_mask_rcnn/dataset/train/sample.jpg')
print(image_2.shape)
# print(image_2)

# with open('/home/dsd/Desktop/calendar_mask_rcnn/dataset/train/test.jpg', 'wb') as f:
#     f.write(image)


