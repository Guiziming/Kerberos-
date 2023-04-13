import os
import cv2
import sys
import numpy as np

path1 = 'E:\code\mycode\source'
path2 = 'E:\code\mycode\source'

for filename in os.listdir(path1):
    if os.path.splitext(filename)[1] == '.png':
        # print(filename)
        sas = os.path.join(path1, filename)
        img = cv2.imread(sas)
        tem = cv2.resize(img, (600,600))
        print(filename.replace(".png", ".png"))
        newfilename = filename.replace(".png", ".png")
        # cv2.imshow("Image",img)
        # cv2.waitKey(0)
        dst = os.path.join(path2, newfilename)
        cv2.imwrite(dst, tem)
