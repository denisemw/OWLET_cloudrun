#!/bin/bash
conda activate owlet_env

cd /Users/werchd01/OWLET_edited_audio_match

csv_file="/Users/werchd01/Documents/ORCA/orca_maap_trials.csv"
results_dir="/Users/werchd01/Documents/ORCA/2.MAAP_results/"
#dst="/Users/werchd01/Documents/ORCA_maap_finished/"
calib_dir="/Users/werchd01/Documents/ORCA/1.Calibration/"
audio_file="/Users/werchd01/Documents/ORCA/MAAP.wav"
task_file="/Users/werchd01/Documents/ORCA/MAAP.mp4"

for file in "/Users/werchd01/Documents/ORCA/1.MAAP/"*;
do
  ff=$(basename $file)
  f=${ff:0:8} 
  echo "Processing $f subject"
  calib=$(find "$calib_dir" -type f -name "$f*")
  #dst=$dst$ff
  python owlet.py $file $results_dir --video_calib $calib --match_audio $audio_file --LR_tags --add_task_video $task_file --add_trial_markers $csv_file
done
