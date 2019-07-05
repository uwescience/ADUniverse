import pandas as pd
import sqlite3

def hello():
	print("Successfully imported aduSQL")

def dbConnect(dbName = 'aduniverse.db'):
    '''
    :string param dbName: the name of the database to connect to.
    '''
    return sqlite3.connect(dbName)

def createDB(df, con, tablename):
    '''
    This function connects to database DB and creates/modifies a database table tablename with values in df
	df: dataframe to be converted into a database table
	con = sqlite3.Connection object
    tablename: the name of the new or existing database table to write to
    Dependencies: sqlite3, pandas
    
    Example:
    df = pd.read_csv("data.csv", sep=",",header=0)
    conn = sqlite3.connect('mydata.db')
    createDB(df, "new_table")
    '''
    df.to_sql(tablename, con, if_exists = 'replace', index=False)
    return

def select(table, con, cols = "*"):
    '''
	table: database table to select table from
	con = sqlite3.Connection object
    cols (optional): list of columns to select from table. Default is * (all columns)
    Dependencies: sqlite3, pandas
    
    Example:
    conn = sqlite3.connect('mydata.db')
    select("tablename", conn)
    -OR-
    select("tablename", conn, ['col1', 'col2', 'col3'])
    '''
    if type(cols) == list:
        cols.reverse()
        last = cols[0]
        tempcols = ""
        for col in range(0,len(cols)):
            colname = cols.pop()
            if colname == last:
                tempcols = tempcols + colname
            else:
                tempcols = tempcols + colname + ", "
                
        cols = tempcols
    
    SQLstring = "SELECT {} FROM {}".format(cols, table)
    return pd.read_sql_query(SQLstring, con)
