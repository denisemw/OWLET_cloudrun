#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 10:20:32 2023

@author: werchd01
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 29 14:34:16 2022

@author: werchd01
"""

import sys
sys.path.append("eyetracker")

import argparse
from calibration_accuracy import Calibration_Accuracy
import os
from pathlib import Path
import glob


def calibrationfolder(value):
    value = Path(value)
    if not value.is_dir():
        raise argparse.ArgumentTypeError(
            'calibration path must point to a folder')
    extension = 'mp4'
    os.chdir(value)
    results = glob.glob('*calibration*.{}'.format(extension))    
    results2 = glob.glob('*Calibration*.{}'.format(extension))
    if len(results2) > 0: results.append(results2)
    if len(results) == 0:
        raise argparse.ArgumentTypeError(
            'calibration folder must contain calibration.mp4 files')
    return value

def parse_arguments():
    parser = argparse.ArgumentParser(description='OWLET - Online Webcam Linked Eye Tracker')
        
    parser.add_argument('calibration', type=calibrationfolder, help='calibration folder where results should be saved')    

    args = parser.parse_args()
    
    return args

    


if __name__ == '__main__':
    cwd = os.path.abspath(os.path.dirname(__file__))
    args = parse_arguments()
    owlet = Calibration_Accuracy()

    path = args.calibration
    extension = 'mp4'
    os.chdir(path)
    calib_files = glob.glob('*calibration*.{}'.format(extension))
    Calib_files = glob.glob('*Calibration*.{}'.format(extension))
    if len(Calib_files) > 0: calib_files.append(Calib_files)
    os.chdir(cwd)

    # results_df = pd.DataFrame(columns = ["Subject_ID", "FC Visual Complexity"])


    owlet.process_subject(cwd, calib_files,str(args.calibration))
           