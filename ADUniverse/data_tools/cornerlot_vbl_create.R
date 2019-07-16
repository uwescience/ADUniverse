########################################################################
##Convert corner lot to CSV and create final binary corner lot variable
##EA Finchum-Mason
##June 25, 2019
########################################################################
rm(list=ls())
library(dplyr)


setwd("//netid.washington.edu/csde/other/desktop/eafinch/Desktop/Zip Codes")

cor <- read.table('cornerlots.txt', 
                  header = T,
                  sep = ",")

par <- read.csv('parcel_zones.csv', 
                header = T,
                sep = ",")

#isolating sample to only residential properties in single family zones
par_SFR <- par %>%
  filter(PROPTYPE == "R" &
         (ZONING == "SF 5000" | 
            ZONING == "SF 7200" | 
            ZONING == "SF 9600"))

#ensuring no duplicate PINs in either file

par_SFR <- par_SFR %>%
  distinct(PIN, .keep_all = T)

cor <- cor %>%
  distinct(PIN, .keep_all = T)

#mergine together based on PIN

par_SFR <- merge(par_SFR, 
                 cor, 
                 by.x= "PIN", 
                 by.y = "PIN",
                 all = T)

table(par_SFR$FREQUENCY)
sum(is.na(par_SFR$FREQUENCY))

#Generating cornerlot variables, one descriptive string and one binary indicator
par_SFR <- par_SFR %>%
  mutate(FREQUENCY = ifelse(is.na(FREQUENCY), 0, FREQUENCY),
         lottype = ifelse(FREQUENCY == 1,"Street-facing",
                          ifelse(FREQUENCY >= 2, "Corner", 
                                 "Not street-exposed")),
         corner = ifelse(lottype == "Corner", 1, 0)) 

table(par_SFR$lottype)
table(par_SFR$corner)

write.csv(par_SFR, "parcel_SFzone_corner.csv")




