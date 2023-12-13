#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 09:18:46 2023

@author: werchd01
"""


import sys
sys.path.append("/Users/werchd01/OWLET/eyetracker")

import argparse
from calibration_accuracy import Calibration_Accuracy

if __name__ == '__main__':
    import glob
    import os
    cwd = os.path.abspath(os.path.dirname(__file__))
    subdir = "/Users/werchd01/Dropbox/ORCA/Subject_videos/Calibration"
    os.chdir(subdir)
    
    calibVideos = glob.glob('*calibration*.mp4') + glob.glob('*Calibration*.mp4') + glob.glob('*calibration*.mov') + glob.glob('*Calibration*.mov')
    calibVideos = [ x for x in calibVideos if "annotated" not in x ]
    
    os.chdir(cwd)


    owlet = Calibration_Accuracy()
    owlet.process_subject(cwd, calibVideos, subdir)