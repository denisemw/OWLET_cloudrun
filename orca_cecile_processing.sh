#!/bin/bash
CECILEFILES="/Users/werchd01/Documents/ORCA_cecile/*"

conda activate owlet_env

cd /Users/werchd01/OWLET_edited_audio_match

for file in "/Users/werchd01/Documents/ORCA_todo/"*;
do
  f=$(basename $file)
  f=${f:0:8} 
  echo "Processing $f subject"
  calib=$(find /Users/werchd01/Documents/ORCA_calibration -type f -name "$f*")
  python owlet.py $file /Users/werchd01/Documents/ORCA_cecile_results --match_audio

done
