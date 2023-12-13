#loading package
library(tidyverse)
library(imputeTS)

setwd("/Users/werchd01/Dropbox/COPE/VisualAttention/GazeTracking-master/gaze_tracking/csv_output") 
saliency = read.csv("/Users/werchd01/OWLET_edited_audio_match/cecile_saliency_coords.csv")
saliency_coords = saliency$Saliency_xcoord

setwd("/Users/werchd01/CecileResults/") # set your working directory
files <- list.files(pattern = "\\.csv$")

df1 = data.frame(matrix(ncol=4,nrow=length(files), dimnames=list(NULL, c("record_id", "MaxCorr1", "MaxLag1", "Length1"))))
i = 1

for (i in 1:length(files)) {
  max_corr  = NA
  min_corr = NA
  maxlag = NA
  minlag = NA
  file = files[i]
  lt <- read.csv(file, header = T)
  length_lt = nrow(lt)
  if (length_lt >= nrow(saliency)) {
    lt$Saliency_xcoord <- c(saliency_coords, rep(NA, nrow(lt)-length(saliency_coords)))
  }else {
    coords = lt$X.coord
    saliency$X.coord <- c(coords, rep(NA, nrow(saliency)-length_lt)) 
    lt <- saliency
  }
  lt = lt[930:1221,]
  lt = lt %>% filter (! is.na(X.coord) )
  if (nrow(lt) > 100) {
    lt = lt %>% filter (! is.na(Saliency_xcoord) )
    results = ccf(lt$Saliency_xcoord, lt$X.coord, lag.max = 60)
    acfs = results$acf
    max_corr = max(acfs)
    maxlag = which.max(acfs)
    min_corr = min(acfs)
    minlag = which.min(acfs)
  }
  if (nrow(lt)==0  | length_lt > 2600) {
    max_corr = NA
    maxlag = NA
  }
  file = gsub(".csv","",ignore.case = T ,file)
  df1[i, "record_id"] = file
  df1[i, "MaxCorr1"] = max_corr
  df1[i, "MaxLag1"] = maxlag
  df1[i, "Length1"] = length_lt
}

df2 = data.frame(matrix(ncol=4,nrow=length(files), dimnames=list(NULL, c("record_id", "MacCorr2", "MaxLag2", "Length2"))))
for (i in 1:length(files)) {
  max_corr  = NA
  min_corr = NA
  maxlag = NA
  minlag = NA
  file = files[i]
  lt <- read.csv(file, header = T)
  length_lt = nrow(lt)
  if (length_lt >= nrow(saliency)) {
    lt$Saliency_xcoord <- c(saliency_coords, rep(NA, nrow(lt)-length(saliency_coords)))
  }else {
    coords = lt$X.coord
    saliency$X.coord <- c(coords, rep(NA, nrow(saliency)-length_lt)) 
    lt <- saliency
  }
  lt = lt[1350:1550,]
  lt = lt %>% filter (! is.na(X.coord) )
  if (nrow(lt) > 100) {
    lt = lt %>% filter (! is.na(Saliency_xcoord) )
    results = ccf(lt$Saliency_xcoord, lt$X.coord, lag.max = 60)
    acfs = results$acf
    max_corr = max(acfs)
    maxlag = which.max(acfs)
    min_corr = min(acfs)
    minlag = which.min(acfs)
  }
  
  if (nrow(lt)==0  | length_lt > 2600) {
    max_corr = NA
    maxlag = NA
  }
  file = gsub(".csv","",ignore.case = T ,file)
  df2[i, "record_id"] = file
  df2[i, "MaxCorr2"] = max_corr
  df2[i, "MaxLag2"] = maxlag
  df2[i, "Length2"] = length_lt
}

df3 = data.frame(matrix(ncol=4,nrow=length(files), dimnames=list(NULL, c("record_id", "MacCorr3", "MaxLag3", "Length3"))))
for (i in 1:length(files)) {
  max_corr  = NA
  min_corr = NA
  maxlag = NA
  minlag = NA
  file = files[i]
  lt <- read.csv(file, header = T)
  length_lt = nrow(lt)
  if (length_lt >= nrow(saliency)) {
    lt$Saliency_xcoord <- c(saliency_coords, rep(NA, nrow(lt)-length(saliency_coords)))
  }else {
    coords = lt$X.coord
    saliency$X.coord <- c(coords, rep(NA, nrow(saliency)-length_lt)) 
    lt <- saliency
  }
  lt = lt[1596:1968,]
  lt = lt %>% filter (! is.na(X.coord) )
  if (nrow(lt) > 100) {
    lt = lt %>% filter (! is.na(Saliency_xcoord) )
    results = ccf(lt$Saliency_xcoord, lt$X.coord, lag.max = 60)
    acfs = results$acf
    max_corr = max(acfs)
    maxlag = which.max(acfs)
    min_corr = min(acfs)
    minlag = which.min(acfs)
  }
  
  if (nrow(lt)==0  | length_lt > 2600) {
    max_corr = NA
    maxlag = NA
  }
  file = gsub(".csv","",ignore.case = T ,file)
  df3[i, "record_id"] = file
  df3[i, "MaxCorr3"] = max_corr
  df3[i, "MaxLag3"] = maxlag
  df3[i, "Length3"] = length_lt
}

df4 = data.frame(matrix(ncol=4,nrow=length(files), dimnames=list(NULL, c("record_id", "MacCorr4", "MaxLag4", "Length4"))))
for (i in 1:length(files)) {
  max_corr  = NA
  min_corr = NA
  maxlag = NA
  minlag = NA
  file = files[i]
  lt <- read.csv(file, header = T)
  length_lt = nrow(lt)
  if (length_lt >= nrow(saliency)) {
    lt$Saliency_xcoord <- c(saliency_coords, rep(NA, nrow(lt)-length(saliency_coords)))
  }else {
    coords = lt$X.coord
    saliency$X.coord <- c(coords, rep(NA, nrow(saliency)-length_lt)) 
    lt <- saliency
  }
  lt = lt[1990:2282,]
  lt = lt %>% filter (! is.na(X.coord) )
  if (nrow(lt) > 100) {
    lt = lt %>% filter (! is.na(Saliency_xcoord) )
    results = ccf(lt$Saliency_xcoord, lt$X.coord, lag.max = 60)
    acfs = results$acf
    max_corr = max(acfs)
    maxlag = which.max(acfs)
    min_corr = min(acfs)
    minlag = which.min(acfs)
  }
  
  if (nrow(lt)==0  | length_lt > 2600) {
    max_corr = NA
    maxlag = NA
  }
  file = gsub(".csv","",ignore.case = T ,file)
  df4[i, "record_id"] = file
  df4[i, "MaxCorr4"] = max_corr
  df4[i, "MaxLag4"] = maxlag
  df4[i, "Length4"] = length_lt
}

df_all = merge(df1, df2, by = "record_id", all.x= T, all.y=T)
df_all = merge(df_all, df3, by = "record_id", all.x= T, all.y=T)
df_all = merge(df_all, df4, by = "record_id", all.x= T, all.y=T)
df_all$MaxCorr_Avg = rowMeans(df_all[, c("MaxCorr1", "MaxCorr2", "MaxCorr3", "MaxCorr4")], na.rm=T)
df_all = df_all[, c("record_id", "MaxCorr_Avg")]
write.csv(df_all, "/Users/werchd01/crosscor_results.csv", na="", row.names = F)
