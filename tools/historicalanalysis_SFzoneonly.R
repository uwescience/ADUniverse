rm(list=ls())
library(dplyr)
library(tidyr)
library(ggplot2)

setwd('~/Desktop/DSSG2019')

d <- read.csv('adu_finalanalytic.csv',
              header = T)

table(d$ADU_all)

#Verifying the distribution of permitted ADUs in zoning
adu <- d %>%
  group_by(ZONING_DES, ZONING) %>%
  summarize(n = n(),
            sum_adu = sum(ADU_all))

write.csv(adu, "adu_depvar_distributionbyzone.csv")

#Looking at the ADUs listed in Lowrise 1 zones:
adu_LR <- d %>%
  filter(ADU_all == 1 & ZONING_DES == "Lowrise 1")

#Subsetting the sample, first by whether the parcel
#is located within a single-family zone.
ds <- d %>%
  filter(ZONING_DES == "Single Family 5000" | 
           ZONING_DES == "Single Family 7200" | 
           ZONING_DES == "Single Family 9600" ) %>%
  filter(SQFTLOT >= 4000) %>%
  filter(!is.na(SHORELINE_))

table(ds$ADU_all) #N = 1842 ADUs

#Checking which zoning categories the other ADU
#parcels are in
#dns <- d %>%
#  filter(ZONING_DES != "Single Family 5000" & 
#           ZONING_DES != "Single Family 7200" & 
#           ZONING_DES != "Single Family 9600" &
#           ZONING_DES != "Lowrise 1") %>%
#  filter(ADU_all == 1)

#table(dns$ZONING_DES)
#Appears to be some in neighborhood residential-commercial
#as well as in lowrise categories.  Running separate analysis
#with the entire sample of parcels, excluding industrial and
#major institutions.

#First splitting up the ADUs into AADU and DADUs

ds <- ds %>%
  mutate(DADU = ifelse(ADU_all == 1 & type_occ == "DADU", 1, 0),
         AADU = ifelse(ADU_all == 1 & type_occ != "DADU", 1, 0))
table(ds$AADU, ds$DADU)

#Beginning with basic parcel-level characteristics, i.e.
#lot size and ECA categorization.

ds_desc <- ds %>%
  group_by(AADU, DADU) %>%
  summarize(n = n(),
            mean_lotsize = mean(SQFTLOT, na.rm = TRUE),
            sd_lotsize = sd(SQFTLOT, na.rm = TRUE),
            prop_steepslope = mean(Parcel_onS, na.rm = TRUE),
            prop_flood = mean(Parcel_Flood,na.rm = TRUE),
            prop_landfill = mean(Parcel_LandF, na.rm = TRUE),
            prop_peat = mean(Parcel_Peat, na.rm = TRUE),
            prop_potentialslide = mean(Parcel_PoteSlide, na.rm = TRUE),
            prop_riparian = mean(Parcel_Riparian, na.rm = TRUE))

write.csv(ds_desc, "lotsize_ECA_descriptives.csv")

#kernel density plots for lot size
#removing outliers
kdens_lotsize <- ggplot(ds, aes(x = SQFTLOT)) + 
  geom_density() + 
  xlim(4000,10000) +
  ggtitle("Distribution of Lot Size, by DADU") + 
  geom_vline(xintercept = 6600, color = "red")

kdens_lotsize

#Running simple bivariates to of land characteristics against DADU 
mod_ls_DADU <- glm(DADU ~ SQFTLOT, 
                   data = ds, 
                   family = binomial(link = "logit"))
summary(mod_ls_DADU)
#smaller lot sizes associated with DADU construction, 
#probably due to the fact that DADUs are built in denser
#neighborhoods that have inherently smaller lots.  Likely
#going to find this correlated with neighborhood and sub-neighborhood

#ignorning landfill and riparian based on lack of variation (all zeros)
mod_ss_DADU <- glm(DADU ~ Parcel_onS, 
                   data = ds, 
                   family = binomial(link = "logit"))
summary(mod_ss_DADU) #DADU less likely on steep slope

mod_fl_DADU <- glm(DADU ~ Parcel_Flood, 
                   data = ds, 
                   family = binomial(link = "logit"))
summary(mod_fl_DADU) #DADU less likely on flood

mod_peat_DADU <- glm(DADU ~ Parcel_Peat, 
                   data = ds, 
                   family = binomial(link = "logit"))
summary(mod_peat_DADU) #DADU more likely on Peat, no theoretical explanation for this

mod_pslide_DADU <- glm(DADU ~ Parcel_PoteSlide, 
                     data = ds, 
                     family = binomial(link = "logit"))
summary(mod_pslide_DADU) #unrelated, ignoring from here on

##Descriptive analysis of census/demographic data

ds_desc <- ds %>%
  group_by(AADU, DADU) %>%
  summarize(n = n(),
            mean_medage = mean(median_age, na.rm = T),
            sd_medage = sd(median_age, na.rm = T),
            mean_totpop = mean(total_population, na.rm = T),
            sd_totpop = sd(total_population, na.rm = T),
            mean_nonwhite = mean(non_white., na.rm = T),
            sd_nonwhite = sd(non_white., na.rm = T),
            mean_pubtrans = mean(public_trans._to_work, na.rm = T),
            sd_pubtrans = sd(public_trans._to_work, na.rm = T),
            mean_hhinc = mean(median_hh_income, na.rm = T),
            sd_hhinc = sd(median_hh_income, na.rm = T),
            mean_pcinc = mean(per_capita_income, na.rm = T),
            sd_pcinc = sd(per_capita_income, na.rm = T),
            mean_owocc = mean(owner_occupied., na.rm = T),
            sd_owocc = sd(owner_occupied., na.rm = T),
            mean_rentocc = mean(renter_occupied., na.rm = T),
            sd_rentocc = sd(renter_occupied., na.rm = T),
            mean_medrent = mean(median_rent, na.rm = T),
            sd_medrent = sd(median_rent, na.rm = T),
            mean_medhv = mean(median_house_value, na.rm = T),
            sd_medhv = sd(median_house_value, na.rm = T),
            mean_colldeg = mean(college_degree., na.rm = T),
            sd_colldeg = sd(college_degree., na.rm = T),
            mean_kids = mean(own_kids_under18., na.rm = T),
            sd_kids = sd(own_kids_under18., na.rm = T),
            mean_hhsize = mean(HH_size.y, na.rm = T),
            sd_hhsize = sd(HH_size.y, na.rm = T))

write.csv(ds_desc, "demos_descriptives.csv")
