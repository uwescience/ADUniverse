#######################################################
##Sq.footage analysis for DADU, ADU, and non-adopters
##EA Finchum-Mason
##6/22/2019
#######################################################     

library(dplyr)
library(ggplot2)

setwd("//netid.washington.edu/csde/other/desktop/eafinch/Desktop/Zip Codes")

parcel_permit <- read.csv('parcel_permit.csv', header=T)

#table(parcel_permit$ADU, parcel_permit$DADU)
table(parcel_permit$PRES_USE_DESC.x)

##Creating descriptive table of lot size by description of present land use
##and ADU/DADU presence
desc_ADU <- parcel_permit %>%
  group_by(PRES_USE_DESC.x, ADU, DADU) %>%
  summarize(n = n(),
            mean_lotsize = mean(GEOM_AREA.x, na.rm=T),
            sd_lotsize = sd(GEOM_AREA.x, na.rm=T))

##Merging parcel_zones data
zones <- read.csv('parcel_zones.csv', header=T)
zones <- zones %>%
  distinct(PIN, .keep_all=T) %>%
  select(PIN, ZONING, ZONELUT, ZONELUT_DESC)

##ppz = "parcel_permit_zone"
ppz <- merge(parcel_permit, zones, by.x="PIN", by.y="PIN")

##Rerunning descriptives for zoning categories
desc_ADU <- ppz %>%
  filter(ZONING=="SF 5000" | ZONING == "SF 5000-PUD" | ZONING == "SF 7200" | ZONING == "SF 9600") %>%
  group_by(ZONING, ADU, DADU) %>%
  summarize(n = n(),
            mean_lotsize = mean(GEOM_AREA.x, na.rm=T),
            sd_lotsize = sd(GEOM_AREA.x, na.rm=T))

##Generating ADU/DADU var for boxplot rendering

ppz$binary_ADU <- ifelse(ppz$ADU==1, "ADU",
                         ifelse(ppz$DADU==1, "DADU", "NONE"))

table(ppz$binary_ADU)

##Subsetting the ppz file to include only SF zoned areas

ppz_sf <- ppz %>%
  filter(ZONING=="SF 5000" | ZONING == "SF 5000-PUD" | 
           ZONING == "SF 7200" | ZONING == "SF 9600")

##Mapping out lot size distributions 

sqft_bp_5000 <- ggplot(ppz_sf %>% filter(ZONING=="SF 5000" | ZONING == "SF 5000-PUD"),
                  aes(x=binary_ADU, y=GEOM_AREA.x))+
                  geom_boxplot()+
                  ylim(0,6000) +
                  xlab("ADU structure")+
                  ylab("Lot Area, sqft")+
                  ggtitle("SF 5000/5000-PUD Zoned Parcels")
sqft_bp_5000

sqft_bp_7200 <- ggplot(ppz_sf %>% filter(ZONING=="SF 7200"),
                       aes(x=binary_ADU, y=GEOM_AREA.x))+
  geom_boxplot()+
  ylim(0,8000) +
  xlab("ADU structure")+
  ylab("Lot Area, sqft")+
  ggtitle("SF 7200 Zoned Parcels")

sqft_bp_7200

sqft_bp_9600 <- ggplot(ppz_sf %>% filter(ZONING=="SF 9600"),
                       aes(x=binary_ADU, y=GEOM_AREA.x))+
  geom_boxplot()+
  ylim(0,10000) +
  xlab("ADU structure")+
  ylab("Lot Area, sqft")+
  ggtitle("SF 9600 Zoned Parcels")

sqft_bp_9600

write.csv(desc_ADU, "desc_ADU.csv")
ggsave("sqft_bp_5000.jpg", sqft_bp_5000)
ggsave("sqft_bp_7200.jpg", sqft_bp_7200)
ggsave("sqft_bp_9600.jpg", sqft_bp_9600)


