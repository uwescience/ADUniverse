########################################################################
##Corner lot analysis, SF residential parcels only
##EA Finchum-Mason
##June 25, 2019
########################################################################
rm(list=ls())
library(dplyr)

setwd("//netid.washington.edu/csde/other/desktop/eafinch/Desktop/Zip Codes")

adu <- read.csv('adufile.csv',
                header = T,
                sep = ",")


par_SFR <- read.csv('parcel_SFzone_corner.csv', 
                header = T)

adu <- adu %>%
  mutate(indic = ifelse(ADU == 1,0,1)) %>%
  filter(indic == 0)

#Merging corner lot and adu data

par_SFR_adu <- merge(par_SFR, adu, by.x = 'PIN', by.y = 'PIN', all.x = T)

par_SFR_adu <- par_SFR_adu %>%
  distinct(PIN, .keep_all = T)

#need updated ADU count to run final descriptives

crl_desc <- par_SFR_adu %>%
  group_by(ADU) %>%
  summarize(n = n(),
            mean_corner = mean(corner))


#Estimting 2118 ADUs (irrespective of ADU/DADU) permits in SF zones with residential
#property type designation.

