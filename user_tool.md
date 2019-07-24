User tools.
Tools to create user tool
Our application is built on top of python's dash package and dependencies, along with the folium library to visualize a map. The initial data set was all provided in csv format. The application is dependent on its connection to the database to operate. Currently, this is fulfilled by housing a local, accessible instance of the SQLite database. Once the application ensures a connection is viable, all relevant information is available through the customized API.

Map Visualization

Financial


****Limitations****
 - For the cost estimation, we understand that each parcel has its own physical characters that may add up or lower the cost of construction. Our estimate is based on appendix 1 of the Environmental Statement Impact (EIS) report on ADUs from the City of Seattle (2018). 
 - For the mortgage calculation, we assumed the homeowner will use home equity loans (HELOC). This assumption is based on the experience of Oregon where most ADU constructors use either cash/savings or home equity loans. The 6.9% APR is the prevailing market rate accessed from Wells Fargo website for a 15-year fixed-rate loan. Both interest rates and rental income are subjected to future market fluctuations, our analysis doesn’t take this into consideration.
 - The approach taken with the application is dependent on the database being hosted locally. Also, as a prototype, the current structure is not readily suitable for hosting as a functioning web application. A potential improvement to that end would be to find a service to web-host our database to ensure all potential users are referencing the same data. The size of our database eliminates some options as solutions. In consideration of Microsoft Azure as a hosting option, changes would be required to shift to that technology.
Our process for generating data and building out our database is not a streamlined process. This limitation curtails any potential future attempts to redo our analysis from scratch. Without access to our revised database, attempts to reproduce our environment could prove quite difficult for a secondary party. Further, there are potential challenges in the event new data surfaces to be added for analysis. Putting a data pipeline in place could go a long way towards supporting the tool’s long-term viability.
How can your work be improved?
 - Some people construct ADU with the intention to sell them in the future. There are a few instances where existing houses with ADU are sold in the market. We didn't provide any information about the potential change in valuations. It would be great if additional information can be obtained about these transactions, then inference on house value changes would be possible.  
