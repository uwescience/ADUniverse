##Creating a clean final analytic dataset

library(dplyr)
library(tidyr)

##Starting with parcel_zones_demos as the base file
##This file includes parcel info present in the original City parcel file,
##as well as zoning information and demographic data derived from the census

parcel_zone_demos <- read.csv('parcel_zone_demos.csv',
                              header = T,
                              sep = ',')

#Detecting and assessing duplicate PINs, which have already been 
#deemed inconsequential to the analysis

pzd_dupl <- data.frame(table(parcel_zone_demos$PIN))
pzd_dupl <- pzd_dupl %>%
  filter(Freq > 1)

parcel_zone_demos <- parcel_zone_demos %>%
  distinct(PIN, .keep_all = T)

parcel_zone_demos <- parcel_zone_demos %>%
  select(-c(X, Join_Cou_1, Join_Count, MTFCC10,
            Shp_Lng, Shap_Ar, TARGET_FID, TARGET_F_1,
            NAMELSA, GEO.id, GEO_ds_))

parcel_zone_demos <- parcel_zone_demos %>%
  mutate(PIN1 = as.factor(PIN))

#Base file has 237,886 observations of 57 variables

##Adding in ADU data

adu <- read.delim2('Export_Output_3.txt',
                   header = T,
                   sep = ',')

typeof(adu$PIN)

adu_dupl <- data.frame(table(adu$PIN))
adu_dupl <- adu_dupl %>%
  filter(Freq > 1)

adu1 <- adu %>%
  distinct(PIN, .keep_all = T)

adu1 <- adu1 %>%
  select(-c(TARGET_FID, Field1, Join_Count, type_name, comp_plan1, 
            comp_plan_,
            cra_no, geoid10, sort_perm, source,
            GEOM_AREA, GEOM_PERIMETER,
            demo, net_units, sleeping_r, value, xcoord, ycoord,
            status_col))

adu1 <- adu1 %>%
  mutate(PIN1 = as.factor(PIN))

##Renaming sqft, proptype, and taxpayer

#colnames(adu1)[colnames(adu1)=="PROPTYPE"] <- "PROPTYPE_adufile"
#colnames(adu1)[colnames(adu1)=="SQFTLOT"] <- "SQFTLOT_adufile"
#colnames(adu1)[colnames(adu1)=="TAXPAYER"] <- "TAXPAYER_adufile"
#colnames(adu1)[colnames(adu1)=="address"] <- "ADDRESS_adufile"
#colnames(adu1)[colnames(adu1)=="STR_ZIP"] <- "ZIP_adufile"

#Merging parcels, zone, demo base file with dependent variable file

pzda <- merge(parcel_zone_demos,
              adu1,
              by = "PIN1",
              all = T)

##Finding the 212 errant PINS - the address, proptype, and sqft data for these
##parcels comes from the adu file, rather than the base file.

missdata <- pzda %>%
  filter(is.na(PIN1))

##The data for the 212 observations with novel pins can be found under the 
##variable names redressed above.

#n_occur <- data.frame(table(pzda$PIN))

#n_occur <- n_occur %>%
#  filter(Freq > 1)

#rm(n_occur)

##No duplicates - the 212 are additional parcel identification numbers

table(pzda$ADU)

##Adding in the neighborhood data

neighborhood <- read.delim2('ZNP.txt',
                            header = T,
                            sep = ",")

nbhd1 <- neighborhood %>%
  select(-c(Join_Count, Join_Cou_1, Join_Cou_2, Join_Cou_3,
            Join_Cou_4, Join_Cou_5, Join_Cou_6, MAJOR, MAJOR_1,
            MAJOR_12, ZONEID, ZONING, ZONELUT, ZONELUT_DE, PRESENTU_1,
            PROPTYPE_1, PROPTYPE_2, SQFTLOT_1, SQFTLOT_12, PLATNAME_1,
            PLATNAME_2, PLATLOT_1, PLATLOT_12, PLATBLOC_1, PLATBLOC_2,
            TAXPAYER_1, TAXPAYER_2, STR_HOUS_1, STR_HOUS_2, STR_PREF_1,
            STR_PREF_2, CONTRACT_1, CONTRACT_2, CONTRACT_3, CONTRACT_4,
            HISTORIC_1, HISTORIC_2, HISTORIC_3, HISTORIC_4, ORDINANCE1,
            SHORELIN_1, SHORELIN_2, SHORELIN_3, SHORELINE1, PIN_1, PIN_12,
            TARGET_F_1, TARGET_F_2, TARGET_F_3, TARGET_F_4, TARGET_F_5,
            TARGET_F_6, OBJECTID_1, OBJECTID_2, OBJECTID_3, OBJECTID_4, 
            OBJECTID_5, OBJECTID_6, HISTORIC_P, PEDESTRI_1,
            PEDESTRI_2, PEDESTRI_3, PEDESTRI_4, PEDESTRI_5,
            MINOR, GEOM_AREA, GEOM_PERIM, GEOM_ARE_1, GEOM_PER_1,
            GEOM_ARE_2, GEOM_PER_2, PROPTYPE, SQFTLOT, PLATNAME,
            PLATLOT, PLATBLOCK, STR_MOD, STR_NAME, STR_HOUSE, STR_NAME_1,
            STR_NAME_2, STR_MOD, STR_TYPE, STR_TYPE_1, STR_TYPE_2,
            STR_SUFF, STR_SUFF_1, STR_SUFF_2, TAXPAYER, PRESENTUSE, PRES_USE_D,
            ADDRESS, CONTRACT, ORDINANCE, EFFECTIVE, EFFECTIVE_, EFFECTIVE1, STR_PREF,
            STR_ZIP, SHORELINE, MHA_1, MHA_12, MHA_VALU_1, MHA_VALU_2, MIO_NAME_1,
            MIO_NAME_2, CONTRACT_P, CONTRACT, CONTRACT_2, CONTRACT_1, CONTRACT_3,
            CONTRACT_4, LIGHTRAI_1, LIGHTRAI_2, LIGHTRAI_3, LIGHTRAIL, LIGHTRAIL1,
            SHAPE_Leng, SHAPE_Le_1, SHAPE_Ar_4, SHAPE_Le_2, SHAPE_Le_2, SHAPE_Le_3,
            SHAPE_Ar_1, SHAPE_Ar_2, SHAPE_Ar_3, SHAPE_Ar_5, SHAPE_Ar_6, SHAPE_Ar_7,
            SHAPE_Ar_8, PERIMETER, PERIMETE_1, PERIMETE_2, FID_Zone_1,
            FID_Zoned1, FID_Zoned_, FID_Zone_2, FID_Zone_2, FID_Zone_3, FID_Zone_4,
            FID_Zone_5, FID_Zone_6, FID_Zone_7, FID_Zone_8, MINOR_1, MINOR_12, PRESENTU_1,
            PRESENTU_2, PRES_USE_2, STR_MOD_1, STR_MOD_12, STR_ZIP_1, STR_ZIP_12,
            ADDRESS_12, ZONEID_1, ZONING_1, ZONEID_12, ZONING_12, 
            ORDINANC_1, EFFECTIV_1, EFFECTIV_2, EFFECTIV_3, EFFECTIVE_, EFFECTIVE,
            OVERLAY_1, OVERLAY_12, CLASS_DE_1, CLASS_DE_2, ZONELUT_1, ZONELUT_12,
            ZONELUT_DE, ZONELUT__1, ZONELUT__2, DETAIL_D_1, DETAIL_D_2, ZONING_D_1,
            ZONING_D_2, BASE_ZON_1, BASE_ZON_2, ZONING_P_1, ZONING_P_2, BZONEID_1,
            BZONEID_12, ELEV_1, ELEV_12, AREA_, FILENUMBER, FILENUMB_1, CONSULTA_1,
            CONSULTANT, SWJOB, SWJOB_1, CONFIDENTI, SLOPEHEI_1, REPAIRTY_1, REPAIRTYPE,
            REPAIREFFE, REPAIREF_1, FIELDCHE_1, FIELDCHECK, PUBLIC_, PUBLIC1,
            SHAPE_L_11, SHAPE_Le_4, SHAPE_Le_5, SHAPE_Le_6, SHAPE_Le_7, 
            SHAPE_Le_8, SHAPE_Le_9, Parcels__5, IZ_1, IZ_12, CATEGORY_1, CATEGORY_2,
            OBJECTID_1, OBJECTI_10, OBJECTID_2, OBJECTID_3, OBJECTID_4, OBJECTI_11,
            OBJECTI_12, OBJECTID_5, OBJECTID_6, OBJECTID_7, OBJECTID_8, OBJECTID_9,
            OBJECTI_10, OBJECTI_13, OBJECTI_14, FID_L22D_1, FID_L22DPD, KSLIDE1,
            KSLIDE_I_1, SW_ID_1, DECADE_1, LOCATION_1, NEIGHBOR_1, TDATE_1,
            DTDATE_1, YEAR1, MONTH1, DAY1, SLOPEHEI_1, SLIDETYP_1,
            DEBRISFL_1, SIZE1, VEGETATI_1, TOPOGRAP_1, GEO1_1, GEO2_1,
            GEO3_1, GEO4_1, NATURAL1, GRNDWTR_1, SURFACEW_1, SURFACED_1,
            WEATHER_1, FILL_CUT_1, ROADFILL_1, PIPELEAK_1, HUMANINF_1, TRENCHFI_1,
            DAMAGE_1, FIELDCHE_1, YSNSLIDE_1, DATECONF_1, COMMENTS_1, COMMENTS_2,
            COMMENTS_3, COMMENTS_4, COMMENTS_5, INPOTSLI_1, INSTEEPS_1, EVENT_DA_1, 
            PARK_1, UNOPENED_1, Parcels__6, OVERLAY_1, OVERLAY_PR, OVERLAY__1,
            OVERLAY__2)) %>%
  distinct(PIN, .keep_all = T)

nbhd1 <- nbhd1 %>%
  mutate(PIN1 = as.factor(PIN))

table(nbhd1$PIN1)

##Renaming obscure parcel indicators

colnames(nbhd1)[colnames(nbhd1)=="Parcels__1"] <- "Parcel_Flood"
colnames(nbhd1)[colnames(nbhd1)=="Parcels__2"] <- "Parcel_LandF"
colnames(nbhd1)[colnames(nbhd1)=="Parcels__3"] <- "Parcel_Peat"
colnames(nbhd1)[colnames(nbhd1)=="Parcels__4"] <- "Parcel_Riparian"
colnames(nbhd1)[colnames(nbhd1)=="Parcels_on"] <- "Parcel_PoteSlide"
colnames(nbhd1)[colnames(nbhd1)=="Parcels_onS"] <- "Parcel_SteepSlope"

##Merging the neighborhood/environmental files with the parcel, zones, and demographics as well
##as the dependent variable file.

adu_finalanalytic <- merge(pzda, 
                           nbhd1, 
                           by = "PIN1", 
                           all = T)

#Checking the merge - addresses that ought to match, do

mergecheck <- adu_finalanalytic %>%
  select(PIN, ADDRESS, ADDRESS_1) %>%
  filter(ADDRESS_1 != " ")

#Exploring the 212 observations with missing PINs

missdata <- adu_finalanalytic %>%
  filter(is.na(PIN))

##Rejoined observations to PINs in ArcGIS, then exported the data to txt

missdata <- read.delim2('miss_PINs.txt',
                        header = T,
                        sep = ',')

#write.csv(missdata, 'missdata_adu_final.csv') #Exported for further exploration

#The following illustrates that the PINs as factors was sufficient to provide for 
#a good merge
xd <- pzda %>%
  select(PIN1, PIN.y, ADDRESS, address) %>%
  filter(!is.na(address))

##########Creating the ADU_all indicator variable##################################

adu_finalanalytic <- adu_finalanalytic %>%
  mutate(ADU_all = ifelse(is.na(ADU), 0 , 1))

table(adu_finalanalytic$ADU_all)
table(adu_finalanalytic$ZONING_DES)

write.csv(adu_finalanalytic, "adu_finalanalytic.csv")

##Running some descriptives on the dependent variable

adu_desc <- adu_finalanalytic %>%
  group_by(ZONING, ZONING_DES, PROPTYPE) %>%
  summarize(N = n(),
            sum_adu = sum(ADU_all, na.rm = T))

adu_byzone <- adu_finalanalytic %>%
  filter(ZONING_DES == "Residential Small Lot" |
           ZONING_DES == "Single Family 5000" |
           ZONING_DES == "Single Family 7200" |
           ZONING_DES == "Single Family 9600") %>%
  group_by(ZONING_DES) %>%
  summarize(n = n(),
         sum_adu = sum(ADU_all, na.rm = T))

#table(adu_finalanalytic$Parcel_Flood)
#table(adu_finalanalytic$Parcel_LandF)
#table(adu_finalanalytic$Parcel_onS)

colnames(adu_finalanalytic)[colnames(adu_finalanalytic)=="Parcel_onS"] <- "Parcel_SteepSlope"
table(adu_finalanalytic$Parcel_SteepSlope)


