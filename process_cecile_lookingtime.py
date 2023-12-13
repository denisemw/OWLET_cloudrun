#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 10:51:40 2023

@author: werchd01
"""

"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
Assumptions: this code only works when the mom is higher than the baby
"""


import pandas as pd
import os
import glob

def Remove_frames(df):
    """Tags frames where a look away starts (defined as 1 second of looking away over a 1.5 second interval)
    Arguments:
        df (pandas.df): Data frame containing trial information (subid, time, frame, Tag, saccade, lookaway,lookto)
    """
    for i in range(0, len(df.index) - 1):
        if df.loc[i,"Time"] > df.loc[i+1,"Time"]:
            df = df.iloc[0:i,]
            return df
    return df


def Tag_away(df):
    """Tags frames where a look away starts (defined as 1 second of looking away over a 1.5 second interval)
    Arguments:
        df (pandas.df): Data frame containing trial information (subid, time, frame, Tag, saccade, lookaway,lookto)
    """
    for i in range(30, len(df.index)):
        start = i - 30
        prior = start - 1
        tmp_df = df.loc[start:i,]
        count = tmp_df[tmp_df['Tag'] == "away"]['Tag'].count()
        if count > 24 and df.loc[start,"Tag"] == "away":
            if start == 0:
                df.loc[start, "lookaway"] = 2
            elif df.loc[prior, "lookaway"] == 0:
                df.loc[start, "lookaway"] = 2
            else:
                df.loc[start, "lookaway"] = 1 
    return df

def Tag_look(df):
    """Tags frames where a look starts (defined as 1 second of looking away over a 1.5 second interval)
    Arguments:
        df (pandas.df): Data frame containing trial information (subid, time, frame, Tag, saccade, lookaway,lookto)
    """
    prior_look_index = -1
    
    for start in range(0, len(df.index)-30):
        end = start + 30
        prior = start - 1
        tmp_df = df.loc[start:end, ]
        count = tmp_df[tmp_df['Tag'] == "away"]['Tag'].count()
        
        # count < 15 indicates a potential look (1 second of cumulative looking)
        if count < 10 and df.loc[start,"Tag"] != "away":
            tmp_df2 = df.loc[prior_look_index:start, ] 
            
            has_lookaway = tmp_df2[tmp_df2['lookaway'] == 2]['lookaway'].count()
            
            ## edge case for very first trial
            if prior_look_index == -1:
                df.loc[start,"lookto"] = 2
                prior_look_index = start
                    
            # the prior trial did not have a look, set look to 
            elif prior > 0 and df.loc[prior, "lookto"] == 0 and has_lookaway != 0:
                df.loc[start,"lookto"] = 2
                prior_look_index = start
                
            # if the prior trial had a look (marked 1 or 2), set look to 1
            elif start > prior_look_index:
                df.loc[start,"lookto"] = 1 
    return df                   
                
def filter_aways(df):
   """Tags frames where a look away starts (defined as 1 second of looking away over a 1.5 second interval)
   Arguments:
       df (pandas.df): Data frame containing trial information (subid, time, frame, Tag, saccade, lookaway,lookto)
   """
   prior_away_index = 0
   prior_look_index = -1
   for i in range(0, len(df.index)):
       if df.loc[i,"lookaway"] == 2:
           if prior_away_index > prior_look_index:
               df.loc[i,"lookaway"] = 1
           prior_away_index = i
       if df.loc[i,"lookto"] == 2:
           prior_look_index = i                    
   return df
          
def calculate_looking(df):
    df = Remove_frames(df)
    df = Tag_away(df)
    df = Tag_look(df)
    df = filter_aways(df)
    looks = df[df["lookto"] == 2]
    # print(looks)

    looksaway = df[df["lookaway"] == 2]
    # print(looksaway)
    # input()
    
    r = len(looksaway.index)
    r2 = len(df.index)
    print(r, r2)
    looksaway.loc[r] = df.iloc[r2-1,0:6]
  #  print(df.iloc[r2-1,0:6])

    looking_times = pd.DataFrame(columns = ['Total Looking Time', 'Start Time', 'End Time'])
    if (len(looks.index) > 0):
        for i in range(0, len(looks.index)):
            end = looksaway.iloc[i,1]
            start = looks.iloc[i,1]
            total_time = end - start
            looking_times.loc[i] = [total_time, start, end]
    lookingtimes = looking_times
    # print(looking_times)
    # num_saccades = df["Saccade"].sum()
    #num_saccades2 = df["saccade_unfiltered"].sum() 
    total_looking = lookingtimes["Total Looking Time"].sum()
    max_look = lookingtimes["Total Looking Time"].max()
    num_looks = len(lookingtimes["Total Looking Time"])
    # avg_look = total_looking/num_looks
    
    return total_looking, num_looks, max_look





    ## looking times processing steps
    
    ## if start or end is not 0, cut trials
    
    ## 1. Tag frames where a look away starts (defined as > 1 sec of looking away over a 1.5 second interval)
    
    ## 2. determine when a look starts (defined as > 1 sec of looking over a 1.5 second interval)
    
    ## 3. remove away Tags that occur after an away without a look in between the two
    
    ## 4. remove rows that are looking away and create a vector of looking times
    
    ## 5. calculate the total number of saccades, the total looking time, the longest look, & the number of looks


path = '/Users/werchd01/Dropbox/ORCA/Cecile_results/CSVs/'
extension = 'csv'
os.chdir(path)
results = glob.glob('*.{}'.format(extension))

results_df = pd.DataFrame(columns = ["Subject_ID", "Total Looking Time",
                                     "Number of Looks", "Max Look Duration"])


results = ['/Users/werchd01/Downloads/elliot_cecile_Cecile.csv']
for file in results:
    
    df = pd.read_csv(file)
    sub = df.loc[0, "Subject_ID"]
    sub_id = sub.split('_')[0]
    sub = df.loc[0, "Subject_ID"]
    sub_id = sub_id + "_" + sub.split('_')[1]
    
    df["lookaway"] = 0
    df["lookto"] = 0
    total_looking, num_looks, max_look = calculate_looking(df)
    
    results_df = results_df.append({'Subject_ID' : sub_id,
                                    'Total Looking Time' : total_looking, 'Number of Looks' : num_looks,
                                    'Max Look Duration' : max_look}, ignore_index = True)
    
# results_df.to_csv("/Users/werchd01/Dropbox/ORCA/Cecile_results/orca_cecile_results_11.13.23.csv", index=False)
results_df.to_csv("/Users/werchd01/Downloads/elliot_cecile.csv", index=False)
