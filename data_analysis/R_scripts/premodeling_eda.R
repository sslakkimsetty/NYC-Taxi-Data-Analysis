library(tidyverse)
library(dplyr)
library(readr)
library(modelr)
library(measurements)
library(purrr)

p1 <- "/Users/sai/Documents/00 NEU/Semester 1/"
p2 <- "1 DS 5110 - Introduction to Data Management and Processing/"
p3 <- "Project/NYC-Taxi-Data-Analysis/data/green/"

dpath <- paste0(p1, p2, p3)
fname <- "green_samp_locid.csv"

green <- read_csv(paste0(dpath,fname))

slocid <- 80
dlocid <- 188

subset <- green %>% 
  filter(pulocationid == slocid, 
         dolocationid == dlocid)

haversine <- function (slon, slat, dlon, dlat) {
  # Calculates great circle distance between two lon-lat pairs
  
  coord <- c(slon, slat, dlon, dlat)
  degrees <- sapply(coord, deg2rad)
  
  # Haversine formula
  dellon <- degrees[[3]] - degrees[[1]]
  dellat <- degrees[[4]] - degrees[[2]]
  
  a <- sin(dellat/2) ^ 2 + (cos(slat) * cos(dlat) * sin(dellon/2) ^ 2)
  b <- 2 * asin(sqrt(a))
  r <- 3956
  dist <- b * r
  
  return(dist)
}

deg2rad <- function (deg) {
  rad <- (2*pi*deg) / 360
  return(rad)
}

subset %>% 
  filter((!is.na(pickup_longitude))) %>% 
  select(pickup_longitude, pickup_latitude, 
         dropoff_longitude, dropoff_latitude, 
         trip_distance) %>% 
  mutate(haversine_dist = pmap_dbl(list(pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude), 
                                   ~ haversine(..1, ..2, ..3, ..4)), 
         percent = haversine_dist/trip_distance) %>% 
  summarize(median(percent))
  ggplot(aes(x=percent)) + 
  geom_histogram(bins=40)

library(rlist)
l <- list()
for (i in c(1:2)) {
  for (j in c(1:2)) {
    l <- list.append(l, list(i, j))
  }
}
str(l)
