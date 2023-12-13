#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 11:10:40 2023

@author: werchd01
"""

import csv
import pandas as pd
import glob
import os

# Open the file in 'r' mode, not 'rb'
csv_file = open('/Users/werchd01/OWLET/Memory/trial_mappings.csv','r')
aois2 =  pd.read_csv('/Users/werchd01/OWLET/Memory/AOIs.csv')

trials = []
aois = []

# Read off and discard first line, to skip headers
csv_file.readline()

# Split columns while reading
for trial, aoi in csv.reader(csv_file, delimiter=','):
    # Append each variable to a separate list
    trials.append(trial)
    aois.append(aoi)



mydir = "/Users/werchd01/Dropbox/ORCA/Memory_results/CSVs"

os.chdir(mydir)
csvs = glob.glob('*.csv') #+ glob.glob('*.mov')

outdir = "/Users/werchd01/Dropbox/ORCA/Memory_results/CSVs/LookingStatistics"
csvs = ["/Users/werchd01/Downloads/elliot_memory_Memory.csv"]
for mycsv in csvs:
    subname = str(os.path.basename(mycsv))
    subname = subname[0:8]
    outfile = outdir + "/" + subname + "_LookingStatistics.csv"
    
    print(mycsv)

        
    f = open(outfile, 'w')
    
    # create the csv writer
    writer = csv.writer(f)
    
    header = ["Trial", "AOI", "RT", "DwellTime_AOI", "DwellTime_Screen"]
    # write a row to the csv file
    writer.writerow(header)
    
    df =  pd.read_csv(mycsv)
    
    for i in range(len(df)): 
        for j in range(len(aois2)):
            if df.loc[i, "X-coord"] in range(aois2.loc[j, 'X1'],aois2.loc[j, 'X2']) \
                and df.loc[i, "Y-coord"] in range(aois2.loc[j, 'Y1'],aois2.loc[j, 'Y2']):
                df.loc[i, "Tag"] = aois2.loc[j, 'AOI']
                break
    df.to_csv(mycsv, index = False)
            
    
    count = 0
    frametime = df.loc[1, "Time"] - df.loc[0, "Time"]
    for trial in trials:
        idx = df[df['Trial'] == trial].index
        if len(idx) > 0:
            start = idx[0]
            print(trial, start)
            aoi = aois[count]
            rt = None
            if count + 1 < len(trials):
                end = df[df['Trial'] == trials[count + 1]].index[0]
            else:
                end = len(df) - 1
            end2 = end+30
            if end2 >= len(df): end2 = len(df) - 1 # extend search for RT to 1 second past trial
            for row in range(start, end2):
                if df.loc[row, "Tag"] == aoi:
                    rt = df.loc[row, "Time"] - df.loc[start, "Time"]
            print(end)
            df_trial = df.loc[start:end]
            numframes_aoi = df_trial[df_trial['Tag'] == aoi].index
            dwell_time_aoi = len(numframes_aoi) * frametime
            numframes_looking = df_trial[df_trial['Tag'] != 'away'].index
            dwell_time_screen = len(numframes_looking) * frametime
            writer.writerow([trial, aoi, rt, dwell_time_aoi, dwell_time_screen])
        count += 1
            
    # close the file
    f.close()
                            