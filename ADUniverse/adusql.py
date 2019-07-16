import pandas as pd
import sqlite3

def hello():
    print("Successfully imported adusql")

class Connection:
    def __init__(self, dbname = "aduniverse.db"):
        '''
        :string param dbname: the name of the database to connect to.
        '''
        self.dbname = dbname
        self.conn = None
        self.connected = False

    def connect(self):
        self.conn = sqlite3.connect(self.dbname)
        self.connected = True

    def createTable(self, df, tablename):
        '''
        This function creates/modifies a database table tablename with values in df
        :pandas DataFarme param df: dataframe to be converted into a database table
        :string param tablename: the name of the new or existing database table to write to
        Dependencies: sqlite3, pandas
        
        Example:
        df = pd.read_csv("data.csv", sep=",",header=0)
        obj.createTable(df, "new_table")
        Depend
        '''
        df.to_sql(tablename, self.conn, if_exists = 'replace', index=False)
        
    def select(self, tablename, cols = "*"):
        '''
        :string param table: database table to select table from
        :list param cols (optional): list of columns to select from table. Default is * (all columns)
        Dependencies: sqlite3, pandas
        
        Example:
        obj.select("tablename")
        -OR-
        obj.select("tablename", ['col1', 'col2', 'col3'])
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
        
        SQLstring = "SELECT {} FROM {}".format(cols, tablename)
        return pd.read_sql_query(SQLstring, self.conn)
        
    def manual(self, tablename, query):
        '''
        :string param query: query the user wants to run against the database
        :list param cols (optional): list of columns to select from table. Default is * (all columns)
        Dependencies: sqlite3, pandas
        
        Example:
        strQuery = "SELECT * FROM table WHERE row1 = 'value1'"
        obj.query(strQuery)
        '''
        return pd.read_sql_query(query, self.conn)
        
    def disconnect(self):
        '''
        Close the database connection
        '''
        self.conn.close()
