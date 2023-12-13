#!/bin/bash
FILES="/Users/werchd01/CecileVideos/*"
conda activate owlet_env

cd /Users/werchd01/OWLET_edited_audio_match
for f in $FILES
do
  echo "Processing $f file..."
  python owlet.py $f /Users/werchd01/CecileResults --embedded_calib --match_audio

done