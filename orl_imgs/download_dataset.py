#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import os
import numpy as np
import random
from sklearn.datasets import fetch_olivetti_faces
from scipy.fftpack import dct
from sklearn.metrics import accuracy_score

# for i in range(0, 40):
#     os.mkdir(str(i))

data_images = fetch_olivetti_faces()
keys = {}
for i in range(0, 40):
    keys[i] = 0
for (img, img_class) in zip(data_images['images'], data_images['target']):
    keys[img_class] += 1
    cv2.imwrite(str(img_class) + '/' + str(keys[img_class]) + '.png', 255 * img)
