import numpy as np
import pandas as pd
import re
import sqlite3
from common_data import app_data
zipcode = 0


def hello():
    print("Successfully imported adusql")


class Connection:
    def __init__(self, dbname="adunits.db"):
        '''
        :string param dbname: the name of the database to connect to.
        '''
        self.dbname = dbname
        self.conn = None
        self.connected = False

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.dbname)
        except:
            raise ValueError("Cannot connect to DataBase %s" % self.dbname)

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
        self.connect()
        df.to_sql(tablename, self.conn, if_exists='replace', index=False)
        self.disconnect()

    def insert(self, df, tablename):
        '''
        This function inserts data into a database table tablename with values in df
        :pandas DataFarme param df: dataframe with values to be insertted into a database table
        :string param tablename: the name of the new or existing database table to write to
        Dependencies: sqlite3, pandas

        Example:
        df = pd.read_csv("data.csv", sep=",",header=0)
        obj.createTable(df, "new_table")
        Depend
        '''
        self.connect()
        df.to_sql(tablename, self.conn, if_exists='append', index=False)
        self.disconnect()

    def select(self, tablename, cols="*"):
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
            for col in range(0, len(cols)):
                colname = cols.pop()
                if colname == last:
                    tempcols = tempcols + colname
                else:
                    tempcols = tempcols + colname + ", "

            cols = tempcols

        self.connect()
        SQLstring = "SELECT {} FROM {}".format(cols, tablename)
        data = pd.read_sql_query(SQLstring, self.conn)
        self.disconnect()
        return data

    def manual(self, query):
        '''
        :string param query: query the user wants to run against the database
        Dependencies: sqlite3, pandas

        Example:
        strQuery = "SELECT * FROM table WHERE row1 = 'value1'"
        obj.query(strQuery)
        -OR-
        '''
        self.connect()
        data = pd.read_sql_query(query, self.conn)
        self.disconnect()
        return data

    def disconnect(self):
        '''
        Close the database connection
        '''
        self.conn.close()

    def getParcelCoords(self, PIN):
        '''
        Retrieve the parcel long/lat coordinates for a specific address
        '''
        self.connect()
        searchStr = "select p.*,g.*,d.*,m.ADU FROM Parcels p left join ParcelGeo g on p.PIN = g.PIN \
            left join ParcelDetails d on p.PIN = d.PIN left join Permits m on p.PIN = m.PIN \
            WHERE p.PIN = '{}'".format(PIN)
        data = self.manual(searchStr)
        self.disconnect()
        return data

    def getZipcode(self, PIN):
        '''
        Retrieve the zipcode of an address
        '''
        self.connect()
        searchStr = "select p.zipcode   \
            FROM Parcels p  \
            WHERE p.PIN = '{}'".format(PIN)
        global zipcode
        zipcode = self.manual(searchStr)
        return zipcode

    def getNeighbors(self, df):
        '''
        Retrieve the neighbor around a specific coordinates
        '''
        self.connect()

        lat = round(df.coordY[0], 2)
        lon = round(df.coordX[0], 2)

        searchStr = "SELECT per.pin, per.adu_type, pd.year_issue, par.address, par.latitude, par.longitude \
                    FROM Permits per \
                    LEFT JOIN Parcels par on per.PIN = par.PIN  \
                    LEFT JOIN PermitDetails pd on per.PIN = pd.PIN \
                    where par.latitude like '{0}%' AND par.longitude like '{1}%' \
                    ".format(lat, lon)

        data = self.manual(searchStr)
        data['dist'] = np.sqrt((data['latitude'] - df.coordY[0])**2 +
                               (data['longitude'] - df.coordX[0])**2)
        data = data.sort_values(by=['dist']).head()
        return data

    def getAddresses(self, sqftlot=0):
        '''
        Retrieve addresses for drop down list population
        :param int zoneid: integer describing zone ID
        '''
        self.connect()
        query1 = "select address, PIN FROM Parcels"
        query2 = "group by address"
        query = "%s where sqftlot > %d %s" % (query1, sqftlot, query2)
        data = self.manual(query)
        self.disconnect()

        return data

    def drop(self, table_name):
        self.connect()
        query = "drop table if exists %s" % table_name
        self.conn.executescript(query)
        self.disconnect()


def keyword_locate(kw, text):
    '''
    This function iterates over entries in the "text" variable, searching for any matches to the "kw" variable.
    Returns an nx1 numpy array of 1s and 0s, 1s indicating a match was found for "kw" in the associated row
    kw: keyword to search for
    text (optional): Pandas series of entries to iterate over.
    '''
    N = len(text)
    text = text.replace(np.nan, 'None')  # Replace NaN values with string 'None'
    arr_match = np.zeros((N, 1))  # define a table of 0s

    iter = 0
    for iter in range(0, N):

        if not text[iter] == 'None':

            # if any instances of the keyword are located...
            if len(re.findall(kw, text[iter])) > 0:
                arr_match[iter] = 1  # indicate a match was found

    return arr_match
