| Dataset      | Description    | Source | File Type | File Size | Indicators |
| ------------- |:-------------:| -----:| ----------: | --------:| ----------:|
| parcels.zip  | Descriptions for all parcels in King County | King County Assessor | Shapefile | 30,016 KB | PIN, lot size, address |
| permits.zip  | All records of permits applied for and issued by King County, including those for accessory dwelling units    |   King County Assessor | Shapefile | 15,352 KB | Type of occupancy, state plane coordinates |





Along with new data we generated to support our analysis, all of it has been structured within in SQLite3 relational database. Some of the new data included geospatial coordinates and parcel shape information obtained using ArcGIS. In order to retrieve and manipulate the database, a module was constructed that uses the sqlite3 package within Python as its foundation. 
