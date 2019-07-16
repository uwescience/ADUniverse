# The input file geodatabase
mygdb <- "/Users/Anaavu/Desktop/Anagha/DSSG/data/parcels.gdb"

require(sf)
#example for layer of ADU Permits that are not under type_occ ADU or DADU
Unspecified_ADU_Permits <- sf::st_read(dsn = mygdb, layer = "Unspecified_ADU_Permits_Only")
summary(Unspecified_ADU_Permits)
plot(Unspecified_ADU_Permits)

#All other layers
ADU_Permits <- sf::st_read(dsn = mygdb, layer = "ADU_Permits") #all ADU_Permits with Zipcodes and Neighborhoods
ADU_Permits_on_ECA <- sf::st_read(dsn = mygdb, layer = "ADU_Permits_on_ECA")
ADU_Permits_on_SlideEvents <- sf::st_read(dsn = mygdb, layer = "ADU_Permits_on_SlideEvents")
ADU_Permits_on_SteepSlopes <- sf::st_read(dsn = mygdb, layer = "ADU_Permits_on_SteepSlopes")
ADU_Permits_on_Wildlife <- sf::st_read(dsn = mygdb, layer = "ADU_Permits_on_Wildlife")
All_Permits_Zipcode_Neighborhoods <- sf::st_read(dsn = mygdb, layer = "All_Permits_Zipcode_Neighborhoods")
ECA_NoWildlife_NoKnownEvents <- sf::st_read(dsn = mygdb, layer = "ECA_NoWildlife_NoKnownEvents")
Seattle <- sf::st_read(dsn = mygdb, layer = "Seattle") #city boundaries
Seattle_roads <- sf::st_read(dsn = mygdb, layer = "Seattle_roads")


#plot(Unspecified_ADU_Permits["lot_size"], max.plot=65)
#plot(st_geometry(Unspecified_ADU_Permits))
  #["lot_size"], max.plot=65)


#OR
# using gdal

# require(rgdal)
# 
# # List all feature classes in a file geodatabase
# subset(ogrDrivers(), grepl("GDB", name))
# fc_list <- ogrListLayers(mygdb)
# print(fc_list)
# 
# # Read the feature class
# fc <- readOGR(dsn=mygdb,layer="Unspecified_ADU_Permits_Only")
# 
# # Determine the FC extent, projection, and 5-number summary of all columns
# summary(fc)
# 
# # View the feature class
# plot(fc)
