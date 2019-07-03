install.packages("sqldf")
install.packages("DBI")
install.packages("RSQLite")

library(sqldf)
library(DBI)
library(RSQLite)

#db <- read.csv.sql("/Users/Anaavu/Desktop/Anagha/DSSG/aduniverse.db")

select <- function(table, cols = '*', cn = con) {
  #table: database table to select table from
  #cols (optional): string of columns to select from table. Default is * (all columns)
  #cn = sqlite3.Connection object
  
  #Example:
  #con <- dbConnect(SQLite(), dbname = "mydata.db")
  #select("tablename")
  #-OR-
  #select("tablename", "col1, col2, col3")
  selString = sprintf("select %s from %s", cols, table)
  dbGetQuery(con, selString)
}

# Ensure there is no existing db connection
if (exists("db")) dbDisconnect(con)

# connect to the sqlite file
con <- dbConnect(SQLite(),  dbname = "aduniverse.db")

# display all table names in the database
dbListTables(con)

# Reads permits table and pull into a data frame
permits <- dbReadTable(con, "permits")

# Select in all entries in parcels db table
dbGetQuery( con,sprintf("select %s from %s", "*", "permits") )

# disconnect from the database
dbDisconnect()
