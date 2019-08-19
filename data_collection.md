
# Data Sources


| Dataset      | Description    | Source | File Type | File Size | Indicators |
| ------------- |:-------------:| -----:| ----------: | --------:| ----------:|
| parcels.zip  | Descriptions for all parcels in King County | King County Assessor | Shapefile | 30,016 KB | PIN, lot size, address |
| permits.zip  | All records of permits applied for and issued by King County, including those for accessory dwelling units    | ZKing County Assessor | Comma Separated Values | 15,352 KB | Type of occupancy, state plane coordinates |
| Residential Buildings.zip | Building and lot dimensions for all residential units in King County | King County Assessor | Comma Separated Values | 24,077 KB | Characteristics of residential dwelling and some accessory structures |
| Zoning.shp | Spatial data identified at the parcel level that indicates the legal zoning status of all parcels in Seattle | Seattle GeoData | Shapefile | | Zoning Characteristics, Shoreline locations |
| Neighborhoods.zip | Spatial data outlining the geographic boundaries of major Seattle neighborhoods | Seattle GIS Open Data | Shapefile | | Neighborhoods and subneighborhoods |
| KingCountyBlockGroups.zip | Spatial data at the Census Block Group level, containing information from the decennial census | King County GIS Open Data | Shapefile | 2 MB | Total population, median household income |
| washington_latest_free.shp.zip | Spatial data on building footprints across Seattle parcels | Open Street Map | Shapefile | 247 MB | Building footprint | 
| rental estimation | Housing sales data | Zillow Economic Dataset | Comma Separated Values |  | Median rent

Data Processing
===============

**King County Assessor Files**
Many of the indicators necessary for historical analysis and user tool creation are readily accessible in the King County Assessor files.  These indicators were linked via the parcel identification number (PIN), or the Major and Minor codes, which constitute the PIN.  Either or both of these identification numbers are available across all King County datasets, thus allowing us to join lot information, residential building characteristics, assessed value, and sales data.

**Identifying ADUs in Permits Data**
City of Seattle provided us with a file containing all of the issued construction permits in Seattle boundaries between 1994 and 2019.  While many ADUs and DADUs could be directly identified the type of occupancy listed in the permit application (i.e. “ADU” or “DADU”), there were some observations for which the type of occupancy was listed as “Single Family”, but for which the comments field suggested the structure to be built was, in fact, an ADU.  Using a SQL query, we were able to extract these observations and add them to the final set of relevant observations for historical analysis. 

**Seattle GeoData Processing**
City of Seattle data on construction permits reflecting the incidence of ADU permitting was not PIN identified, but did contain state plane coordinates that were used to overlay an ESRI shapefile depicting Seattle parcels with the location of permits.  Spatially joining these layers with ArcGIS and R has allowed us to outfit each permit with its unique parcel identifier.  Spatial joins of this nature can sometimes be problematic, depending on the unique relationship between polygons and points, so we were careful to assess the validity of the join by leaving the address field in each file and ensuring that there was a match in these values for each observation.  When all of these variables had been calculated, we ran a spatial autocorrelative measure (Global Moran’s I) on the dataset to determine spatial correlation within identified ADUs and DADUs, finding a low index, so that we could move forward with traditional statistical analyses.

We likewise identified each parcel’s placement on neighborhood, zip code, environmental variables (steep slope, riparian corridors, peat settlements, etc), city zones, and on high tree cover yards. We were then able to measure these parcels’ proximity to other zones, to nearest and frequent transit stops, to alleys and to the shoreline. Their potential demographic characteristics based on their location in a census block and their potential median home value based on their location in a Zillow neighborhood was also calculated. Using ArcGIS tools, we created corner lot, alley lot, and lot coverage indicators by overlaying relevant shapefiles and manipulating intersecting features.

Along with new data we generated to support our analysis, all of it has been structured within in SQLite3 relational database. Some of the new data included geospatial coordinates and parcel shape information obtained using ArcGIS. In order to retrieve and manipulate the database, a module was constructed that uses the sqlite3 package within Python as its foundation. 
