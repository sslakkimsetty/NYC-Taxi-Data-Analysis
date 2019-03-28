library(tidyverse)
library(dplyr)
library(readr)
library(lubridate)

setwd(paste0('~/Documents/00 NEU/Semester 1/', 
          '1 DS 5110 - Introduction to Data Management', 
          ' and Processing/Project/'))

data <- read_csv('data/green_tripdata_2018-01.csv')

data %>% head()

table(data$passenger_count)

table(filter(data, fare_amount < 0)$passenger_count)
table(filter(data, fare_amount < 0)$payment_type)
table(filter(data, fare_amount == 0)$trip_distance) %>% plot()

data %>% select(-payment_type) %>% n_distinct()
data %>% nrow()

data %>% 
  filter(fare_amount<=0) %>% 
  select(fare_amount, trip_distance) %>% 
  ggplot() + 
  geom_jitter(aes(x=trip_distance, y=fare_amount), alpha=0.3) + 
  geom_smooth(aes(x=trip_distance, y=fare_amount)) + 
  coord_cartesian(xlim=c(0,1), ylim=c(-12.5,0))

data %>% 
  filter(trip_distance == 0) %>% 
  select(fare_amount, trip_distance) %>% 
  ggplot() + 
  geom_histogram(aes(x=fare_amount), bins=100)

names(data)

data %>% nrow()

data2 <- data %>% select(lpep_pickup_datetime, lpep_dropoff_datetime, 
                passenger_count, trip_distance, fare_amount, payment_type, tip_amount)

data2 %>% select(-fare_amount) %>% n_distinct()

table(data2$payment_type)

# charges <- read_csv('~/Downloads/Checking1.csv', col_names=F, 
#                     col_types=)
# names(charges) <- c('date', 'charge', 'X3', 'X4', 'desc')
# 
# charges %>% filter(grepl('PURCHASE AUTHORIZED', desc)) %>% as.data.frame() %>% summarize(sum = sum(charge)+349)

data3 <- data2 %>% select(-c(fare_amount, payment_type, tip_amount))
sum(duplicated(data3) | duplicated(data3, fromLast=T))

data %>% filter(payment_type==3, fare_amount!=0) %>% select(payment_type, fare_amount)
