#!/bin/bash

cd /Users/werchd01/Documents/ORCA/1.VPC
start=0;
length=44;
end=$(($start + $length))
echo "$end"
ffmpeg -ss "$start" -to "$duration" -i orca_004_vpc.mov_cropped.mp4 -c orca_004_vpc.mov_cropped2.mp4;