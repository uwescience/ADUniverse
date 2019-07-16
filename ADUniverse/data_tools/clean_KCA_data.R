library(dplyr)
library(tidyr)

setwd('~/Desktop/DSSG2019')

#pin <- read.csv('parcel_zone_demos.csv',
#                header = T)

#pin <- pin %>%
#  select(PIN) %>%
#  distinct(PIN, .keep_all = T)

p <- read.delim("KCA_Parcel.txt",
                 header = T)

#p <- merge(p, pin, by = "PIN", all.y = T)

acc <- read.delim2("KCA_AccessoryStructures.txt",
                   header = T,
                   sep = ",")

typeof(acc$MAJOR)
typeof(acc$MINOR)

#p <- merge(p, acc, by = c('MAJOR', 'MINOR'), all.x = T)

build <- read.delim2('KCA_BuildingCharacteristics.txt',
                     header = T,
                     sep = ",")

#sum_build <- build %>%
#  summarize(n = n(),
#            mean_year = mean(YRBUILT))

build <- build %>%
  select(MAJOR, MINOR, PIN, SQFT1STFLOOR, STORIES, 
         YRBUILT, DAYLIGHTBASEMENT, SQFTFINBASEMENT)

build <- build %>%
  mutate(PIN1 = as.factor(PIN))

#build <- merge(build, pin, by = "PIN")

#build.dupl <- data.frame(table(build$PIN))
#build.dupl <- build.dupl %>%
#  filter(Freq > 1)

#kca <- merge(p, build, by = "PIN")
kca <- kca %>%
  select(-c(OBJECTID.x, OBJECTID.y, MAJOR.x, MAJOR.y,
            MINOR.x, MINOR.y))

kca_desc <- kca %>%
  summary(n = n(),
    year = mean(YRBUILT, na.rm = T))

#Merging the assessor's data with the final analytic dataset
data <- read.csv('adu_finalanalytic.csv',
                 header = T)

data <- data %>%
  select(-c(OBJECTID.x, FID.x, FID.y))

#only merging build data with adu file
data1 <- merge(data, build, by.x = "PIN1", by.y = "PIN1", all.x = T)

data1 <- data1 %>%
  distinct(PIN, .keep_all = T)

table(data1$ADU_all)


##Getting rid of superfluous variables as well as adding a lot coverage approximation
data1 <- data1 %>%
  select(-c(PIN.y))

#translates to ratio of lot covered
data1$LOTCOVERAGE <-  data1$SQFT1STFLOOR / (data1$SQFTLOT + 1)
summary(data1$LOTCOVERAGE)

write.csv(data1, 'adu_finalanalytic.csv')



