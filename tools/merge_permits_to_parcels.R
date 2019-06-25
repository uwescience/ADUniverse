#######################################################
##Linking permits to parcels (and zones as well)
##EA Finchum-Mason
##6/22/2019
#######################################################

library(dplyr)

rm(list=ls())

setwd("//netid.washington.edu/csde/other/desktop/eafinch/Desktop/Zip Codes")

permit_ID <- read.csv('permits_ID.csv', header=T)

permit_ID <- permit_ID %>%
  filter(Join_Count=="1")

permit_ID <- permit_ID %>%
  mutate(ADU = ifelse(type_occ=="ADU",1,0),
         DADU = ifelse(type_occ=="DADU",1,0))

permit_ID <- permit_ID %>%
  distinct(PIN, .keep_all=TRUE)

#Reading in parcel data
parcel <- read.csv('parcels.csv', header=T)

#parcel$duplicate <- ifelse(duplicated(parcel$PIN)=="TRUE",1,0)
#table(parcel$duplicate)
#375 unexplained duplicates removed

parcel <- parcel %>%
  distinct(PIN, .keep_all = TRUE)

#Linking ADU and DADU permits to parcels
parcel_permit <- merge(parcel, permit_ID, by.x="PIN", by.y="PIN", all=T)

table(parcel_permit$ADU)
table(parcel_permit$DADU)

#Replacing missing values with zeros
parcel_permit$ADU[is.na(parcel_permit$ADU)] <- 0
parcel_permit$DADU[is.na(parcel_permit$DADU)] <- 0


write.csv(parcel_permit,'parcel_permit.csv')


