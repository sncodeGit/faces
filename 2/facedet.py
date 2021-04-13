#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from   math     import sqrt
from   imutils  import face_utils
import cv2
import numpy    as np
import imutils
import dlib
# Selfmade
import config   as cfg

def template_matching(target_img_path, template_img_path, threshold=0.8):
    target_img_rgb = cv2.imread(target_img_path)
    target_img_gray = cv2.cvtColor(target_img_rgb, cv2.COLOR_BGR2GRAY)

    template_img = cv2.imread(template_img_path, 0)
    w, h = template_img.shape[::-1]

    res = cv2.matchTemplate(target_img_gray, template_img, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(target_img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
    target_img_rgb = imutils.resize(target_img_rgb, width=350)

    return target_img_rgb

def viola_jones(img_path):
    img = cv2.imread(img_path)
    img = imutils.resize(img, width=350)
    # load the pre-trained model
    classifier = cv2.CascadeClassifier(cfg.HAARCASCADE_FRONTALFACE_FILE)
    # perform face detection
    bboxes = classifier.detectMultiScale(img)
    # print bounding box for each detected face
    for box in bboxes:
        # extract
        x, y, width, height = box
        x2, y2 = x + width, y + height
        # draw a rectangle over the pixels
        cv2.rectangle(img, (x, y), (x2, y2), (0,0,255), 1)
    return img

def symmetry_lines(img_path):
    # initialize dlib's face detector (HOG-based) and then create
    # the facial landmark predictor
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(cfg.SHAPE_PREDICTOR_FILE)

    # load the input image, resize it, and convert it to grayscale
    image = cv2.imread(img_path)
    image = imutils.resize(image, width=350)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # detect faces in the grayscale image
    rects = detector(gray, 1)

    # loop over the face detections
    for (i, rect) in enumerate(rects):
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)
    # convert dlib's rectangle to a OpenCV-style bounding box
    # [i.e., (x, y, w, h)], then draw the face bounding box
    (x, y, w, h) = face_utils.rect_to_bb(rect)
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    # loop over the (x, y)-coordinates for the facial landmarks
    # and draw them on the image
    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
    leftEye = shape[lStart:lEnd]
    rightEye = shape[rStart:rEnd]
    (xl1,yl1)=shape[37]
    (xl2,yl2)=shape[38]
    (xl3,yl3)=shape[40]
    (xl4,yl4)=shape[41]
    cl1 = int(sqrt((xl2-xl1)**2 + (yl2-yl1)**2)/2)
    cl2 = int(sqrt((xl4-xl3)**2 + (yl4-yl3)**2)/2)
    l_start = (xl1+cl1,yl1+cl1)
    l_end = (xl4+cl2,yl4+cl2)

    (xf,yf) = shape[8]
    (xs,ys) = shape[27]
    cv2.line(image,(xf,yf),(xs,ys),(0, 240, 240),3)

    xl1r = xs - (xl1+cl1)
    xl2 = xf - xl1r
    cv2.line(image,(xl2,yf),(xl1+cl1,ys),(255, 0, 0),3)

    (xr1,yr1)=shape[43]
    (xr2,yr2)=shape[44]
    (xr3,yr3)=shape[46]
    (xr4,yr4)=shape[47]
    cr1 = int(sqrt((xr2-xr1)**2 + (yr2-yr1)**2)/2)
    cr2 = int(sqrt((xr4-xr3)**2 + (yr4-yr3)**2)/2)
    r_start = (xr1+cr1,yr1+cr1)
    r_end = (xr4+cr2,yr4+cr2)
    xr1r = (xr1+cr1) - xs
    xr2 = xf + xr1r
    cv2.line(image,(xr2,yf),(xr1+cr1,ys),(255, 0, 0),3)

    (xrf,yrf) = shape[24]
    (xrs,yrs) = shape[10]
    (xlf,ylf) = shape[48]
    (xls,yls) = shape[20]
    return image
