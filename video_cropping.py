#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 21 16:10:21 2023

@author: werchd01
"""

import cv2
import dlib
import os
import numpy as np
import subprocess
import argparse
import librosa
from scipy import signal

def videofile_arg(value):
    if not (value.endswith('.mp4') or value.endswith('.mov') or value.endswith('.m4v')):
        raise argparse.ArgumentTypeError(
            'video file must be of type *.mp4, *.mov, or *.m4v')
    return value

def parse_arguments():
    parser = argparse.ArgumentParser(description='OWLET - Online Webcam Linked Eye Tracker')
    
    parser.add_argument('video', type=videofile_arg, help='the subject video to process (path to video file.')
    args = parser.parse_args()
    
    return args
  
def convert_video_to_audio_ffmpeg(video_file, output_ext="wav"):
    """Converts video to audio directly using `ffmpeg` command
    with the help of subprocess module"""
    # ffmpeg_path = "ffmpeg/ffmpeg"
    # if hasattr(sys, '_MEIPASS'):
    #     mypath = os.path.join(sys._MEIPASS, ffmpeg_path)
    # else:
    #     mypath = os.path.join(os.path.abspath(""), ffmpeg_path)
    # # print (mypath)
        
    filename, ext = os.path.splitext(video_file)
    # print(filename)
    
    subprocess.call(["ffmpeg", "-y", "-i", video_file, f"{filename}.{output_ext}"], 
                stdout=subprocess.DEVNULL,
                stderr=subprocess.STDOUT)
    
    # subprocess.run([mypath, "-i", "-y", video_file, f"{filename}.{output_ext}"], 
    #                 stdout=subprocess.DEVNULL,
    #                 stderr=subprocess.STDOUT)   


def find_offset(subject_audio, task_audio):
    """
    Returns the offset between the subject video and the start of the task
    based on matching the audio patterns using FFT and cross correlations
    
    Arguments:
        subject_audio (wav file): The audio file name of the subject audio
        task_audio (wav file): The audio file name of the task audio
        window (int): The window in which to search for a match within
        
    Returns:
        The time until the task begins in the subject video
    """
    y_within, sr_within = librosa.load(subject_audio, sr=None)
    y_find, sr_find = librosa.load(task_audio, sr=sr_within)

    c = signal.correlate(y_within, y_find, mode='valid', method='fft')
    found=True
    
    peak = np.argmax(c)
    start = round(peak / sr_within, 2) * 1000
    sub_audio_length = librosa.get_duration(y_within, sr_within) * 1000
    task_audio_length = librosa.get_duration(y_find, sr_find) * 1000

    if c[peak] < 90:
        start = 0
        found=False

    end = start + (task_audio_length) + 1000
    
    if end > sub_audio_length:
        end = sub_audio_length
        start = sub_audio_length - task_audio_length
        
    if start < 0: start = 0

    return start, end, sub_audio_length, task_audio_length, found
    
if __name__ == '__main__':
    # _face_detector is used to detect faces
    face_detector = dlib.get_frontal_face_detector()
    cwd = os.path.abspath(os.path.dirname(__file__))
    args = parse_arguments()
    videofile = args.video
  #  videofile = os.path.abspath(os.path.join(cwd, "orca_050_calibration.mp4"))
    cap = cv2.VideoCapture(videofile) 
    found_face = 0
    xList = []
    wList = []
    yList = []
    hList = []
    
    while (cap.isOpened() and found_face < 250):
        frameId = cap.get(1) #current frame number
        ret, frame = cap.read()
    
        if (ret == False):
            break
        
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        height, width = frame.shape
        faces = face_detector(frame)
                
        ## if there are two faces detected, take the lower face
        if len(faces) > 1 and (faces[1].bottom() > faces[0].bottom()):
            face_index = 1
        else:
            face_index = 0
        if len(faces) > 0:
            startY = faces[face_index].top()
            endY = faces[face_index].bottom()
            startX = faces[face_index].left()
            endX = faces[face_index].right()
            face_h = endY - startY
            center_y = startY + (face_h / 2)
            center_x = startX + ((endX - startX) / 2)
            max_w = width
            max_h = height
    
            # verify that the face isn't a stimulus (by checking if the found face is super small)
            if face_h / height > .1:
                found_face += 1  
    
                # changing aspect ratio to 16x9     
                if max_w/max_h > 1.8:
                    max_w = int(max_h / .5625)
                elif max_w/max_h < 1.75:
                    max_h = int(max_w * .5625)
                    
                # zooms in on face if face is too far
                if face_h / max_h < .4:
                    max_h = int(face_h / .4)
                    max_w = int(1.7777*max_h)
                y = int(center_y - int(max_h/2))
                h = int(center_y + int(max_h/2))
                x = center_x - int(max_w/2)
                w = center_x + int(max_w/2)
                
                # make sure new coords aren't out of bounds
                if y < 0: 
                    diffY = abs(y)
                    y = 0
                    h = h + diffY
                if h > height:
                    diffH = h - height
                    h = height
                    y = y - diffH
                if x < 0: 
                    diffX = abs(x)
                    x = 0
                    w = w + diffX
                if w > width:
                    diffW = w - width
                    w = width
                    x = x - diffW
                xList.append(x)
                yList.append(y)
                wList.append(w)
                hList.append(h)
        
    cap.release()
    cv2.destroyAllWindows()
    print("yup")
    
    if len(xList) < 100:
        if width/height > 1.8:
            width = int(height / .5625)
        elif width/height < 1.75:
            height = int(width * .5625)
        w, h, x, y = width, height, 0, 0
    
    else:    
        xList2=np.array(xList)
        x = int(sum(xList2)/len(xList2))
        
        xList2=np.array(yList)
        y = int(sum(xList2)/len(xList2))
        
        xList2=np.array(wList)
        w = int(sum(xList2)/len(xList2)) - x
        
        xList2=np.array(hList)
        h = int(sum(xList2)/len(xList2)) - y
    
   
    # taskAudio = os.path.abspath(os.path.join(cwd, "orca_calibration.wav"))
    # convert_video_to_audio_ffmpeg(videofile)
    # subAudio = videofile[0:-4] + ".wav"
    
    # start, end, sub_audio_length, task_audio_length, found = find_offset(subAudio, taskAudio)
    
    # os.remove(subAudio)
    filename, ext = os.path.splitext(videofile)

    # start = int(start / 1000)
    # end = int(end / 1000)
    
    # min_start = start // 60
    # sec_start = start % 60
    
    # min_end = end // 60
    # sec_end = end % 60
    
    # vals = [str(min_start), str(sec_start), str(min_end), str(sec_end)]
    # for i in range(len(vals)):
    #     if len(vals[i]) < 2:
    #         vals[i] = "0" + vals[i]
        

    # ff_start = "00:" + vals[0] + ":" + vals[1]
    # ff_end = "00:" + vals[2] + ":" + vals[3]

    mystr = "crop=%s:%s:%s:%s" % (w, h, x, y)
    
    # print(ff_start, ff_end, mystr, videofile, filename)
    
    # if found:
    #     subprocess.call(["ffmpeg", "-ss", ff_start, "-to", ff_end, "-i", videofile, "-filter:v", mystr, f"{filename}_calibration.mp4"], 
    #                 stdout=subprocess.DEVNULL,
    #                 stderr=subprocess.STDOUT)
    # else:
    #     ff_end = "00:00:00"


        
    # subprocess.call(["ffmpeg", "-ss", ff_end, "-i", videofile, "-filter:v", mystr, f"{filename}_tasks.mp4"], 
    #             stdout=subprocess.DEVNULL,
    #             stderr=subprocess.STDOUT)
    
    subprocess.call(["ffmpeg", "-i", videofile, "-filter:v", mystr, f"{filename}_tasks.mp4"], 
                stdout=subprocess.DEVNULL,
                stderr=subprocess.STDOUT)