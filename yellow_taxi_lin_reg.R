library(lubridate)
library(tidyverse)
library(dplyr)
library(readr)
library(modelr)
library(tictoc)
data<-read_csv('yellow_data.csv')
part<-resample_partition(data,p=c(train=0.7,test=0.3))
train_dat<-as.tibble(part$train)

train_dat<-train_dat%>%filter(between(price_mile,2,20),between(fare_amount,0,50))
tic('model time')
fit<-lm(fare_amount~trip_distance+week_type*day_shifts,data=train_dat)
toc()
dat<-train_dat%>%mutate(preds=fit$fitted.values)
dat<-dat[,c('preds','pulocationid','dolocationid','fare_amount','trip_distance')]
#plot of fit on training data

ggplot(train_dat)+geom_point(mapping=aes(x=trip_distance,y=fare_amount))+geom_line(mapping = aes(x=trip_distance,y=fit$fitted.values))
pred<-add_predictions(part$test,fit)
test<-as.tibble(part$test)
predvact<-data.frame(pred$pred,test$fare_amount,test$pulocationid,test$dolocationid,test$trip_distance)
print(predvact)
rmse(fit,part$test)


