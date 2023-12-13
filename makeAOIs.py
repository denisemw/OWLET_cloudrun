#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 15:36:16 2023

@author: werchd01
"""

import cv2
import os
import pandas as pd

# CWD = os.path.abspath(os.path.dirname(__file__))
# global CWD
SELECTION_COLOUR = (222,0,222)
WINDOW_NAME = "Select regions with a mouse"
global OUTPUT_IMG
global OUTPUT_FILE
# OUTPUT_IMG = CWD + "/AOIs.png"
# OUTPUT_FILE = CWD + "/AOIs.csv"

def click_select(event, x, y, flags, param):
    global image
    global points
    global aois

    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))
    elif event == cv2.EVENT_LBUTTONUP:
        global cache
        cache = image.copy()
        points.append((x, y))
        n = len(points) / 2
        text = "Area " + str(int(n))
        p1  = points[-2]
        p2 = points[-1]
        aois.append(text)
        if p2[0] < p1[0]: 
            x = p2[0] + 10
        else:
            x = p1[0] + 10
        if p2[1] < p1[1]: 
            y = p2[1] + 20
        else:
            y = p1[1] + 20
        cv2.rectangle(image, points[-2], points[-1], SELECTION_COLOUR, 2)
        
        cv2.putText(image, text, (x,y), cv2.FONT_HERSHEY_DUPLEX, 0.9, SELECTION_COLOUR, 1)
        cv2.imshow(WINDOW_NAME, image)


def show_mouse_select(image_filename, output_filename):
    orig = cv2.imread(image_filename)
    orig = cv2.resize(orig, (960,540))    
    global image
    global cache
    global points
    global aois
    image = orig.copy()
    cv2.namedWindow(WINDOW_NAME)
    global OUTPUT_IMG
    global OUTPUT_FILE
    
    
    global df #= pd.DataFrame(columns = ['AOI', "X1", "Y1", "X2", "Y2"]) 
    global points #= []
    global aois #= []
    cv2.setMouseCallback(WINDOW_NAME, click_select)

    while True:
        cv2.imshow(WINDOW_NAME, image)
        key = cv2.waitKey(1)
        if key == ord('q'): break       # press q to exit
        if key==27:
            points.pop()
            points.pop()
            aois.pop()
            image = cache.copy()
            cv2.imshow(WINDOW_NAME, image)
            

    # Output points and save image
    if len(points)>1:
        
        
        cv2.imwrite(output_filename, image)
        print ("Saved to:", output_filename)
        
        

    cv2.destroyAllWindows()

if __name__=="__main__":
    from sys import argv
    
    CWD=os.path.dirname(argv[1])
    
    mydir = argv[1]
    os.chdir(mydir)
    import glob
    images = glob.glob('*.png') + glob.glob('*.jpg') + glob.glob('*.jpeg')
    
    global OUTPUT_IMG
    global OUTPUT_FILE
    OUTPUT_IMG = CWD + "/AOI_regions.png"
    OUTPUT_FILE = CWD + "/AOIs.csv"
    global aois
    global points
    global df
    df = pd.DataFrame(columns = ['AOI', "X1", "Y1", "X2", "Y2"]) 
    points = []
    aois = []
    
    
    for image in images:
        img_name = os.path.basename(image)
        output_image = mydir + '/AOIS_' + img_name
        show_mouse_select(image, output_image)
        
    points.reverse()
    aois.reverse()
    while len(points) > 1:
        x1, y1 = points.pop()
        x2, y2 = points.pop()
        if x2 < x1:
            tmp = x2
            x2 = x1
            x1 = tmp
        if y2 < y1:
            tmp = y2
            y2 = y1
            y1 = tmp;
        y1 = y1 - 150
        y2 = y2 + 150
        if y1 < 0: y1=0
        if y2 > 540: y2=540
            
        aoi = aois.pop()
        df = df.append({'AOI': aoi, 'X1':x1, 'Y1':y1, 'X2':x2, 'Y2':y2}, ignore_index=True)
        df.to_csv(OUTPUT_FILE)