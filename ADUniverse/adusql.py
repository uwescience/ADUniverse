import numpy as np
import pandas as pd
import re
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
        df.to_sql(tablename, self.conn, if_exists = 'replace', index=False)
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
        df.to_sql(tablename, self.conn, if_exists = 'append', index=False)
        self.disconnect()

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

    def getCoords(self, PIN):
        '''
        Retrieve the long/lat coordinates for a specific address
        '''
        self.connect()
        searchStr = "select latitude, longitude FROM Parcels p WHERE p.PIN = {}".format(PIN)
        data = self.manual(searchStr)
        self.disconnect()

        return data

    def getParcelCoords(self, PIN):
        '''
        Retrieve the parcel long/lat coordinates for a specific address
        '''
        self.connect()
        searchStr = "select * FROM Parcels p join ParcelGeo g on p.PIN = g.PIN join ParcelDetails d on p.PIN = d.PIN WHERE p.PIN = {}".format(PIN)
        data = self.manual(searchStr)
        self.disconnect()
        return data

    def getAddresses(self):
        '''
        Retrieve addresses for drop down list population
        '''
        self.connect()
        searchStr = "select address, PIN FROM Parcels group by address"
        data = self.manual(searchStr)
        self.disconnect()

        return data

def keyword_locate(kw, text):
    '''
    This function iterates over entries in the "text" variable, searching for any matches to the "kw" variable.
    Returns an nx1 numpy array of 1s and 0s, 1s indicating a match was found for "kw" in the associated row
    kw: keyword to search for
    text (optional): Pandas series of entries to iterate over.
    '''
    N = len(text)
    text = text.replace(np.nan, 'None') # Replace NaN values with string 'None'
    arr_match = np.zeros((N,1)) # define a table of 0s

    iter = 0
    for iter in range(0,N):

        if not text[iter] == 'None':

            # if any instances of the keyword are located...
            if len(re.findall(kw,text[iter])) > 0:
                arr_match[iter] = 1 # indicate a match was found

    return arr_match

def adu_dadu(types = 'all', data = None):
    # ADUs/DADUs
    if types == 'all':
        return data.type_occ.eq('ADU') | data.type_occ.eq('DADU')
    elif types == 'adu':
        return data.type_occ.eq('ADU')
    elif types == 'dadu':
        return data.type_occ.eq('DADU')

def excs(types = 'all', data = None):
    if types == 'all':
        # all noted exceptions
        EXCs = data.objectid.eq(72) | data.objectid.eq(117) | data.objectid.eq(595) | data.objectid.eq(622)
        EXCs = EXCs | data.objectid.eq(726) | data.objectid.eq(998) | data.objectid.eq(1064)
        EXCs = EXCs | data.objectid.eq(1249) |  data.objectid.eq(10188) | data.objectid.eq(16818)
    elif types == 'adu':
        # Specifically noted ADU exceptions
        EXCs = data.objectid.eq(117) | data.objectid.eq(998) | data.objectid.eq(10188) | data.objectid.eq(16818)
    elif types == 'dadu':
        # Specifically noted DADU exceptions
        EXCs = data.objectid.eq(72) | data.objectid.eq(595) | data.objectid.eq(622) | data.objectid.eq(726)
        EXCs = EXCs | data.objectid.eq(1064) | data.objectid.eq(1249)

    return EXCs

def sf_adus(types = 'all', data = None):
    # Units under SF
    SF = (np.asarray(data.type_occ == 'SF').reshape(-1,1))*1

    if types == 'all':
        # entries containing "ADU", less those containing "adult"
        ADU_kw = keyword_locate('ADU', text = data.comments) - keyword_locate('adult', text = data.comments)

        # entries containing "accessory dwelling" in the comments
        ADU_text = keyword_locate('accessory dwelling', text = data.comments)
        ADU_kw_text = ((ADU_kw + ADU_text) > 0)*1

        SF = ((SF + ADU_kw_text) > 1)*1

    elif types == 'adu':
        # entries containing "ADU", less those containing "adult" and "DADU"
        not_AADU = keyword_locate('adult', text = data.comments) + keyword_locate('DADU', text = data.comments)
        not_AADU = (not_AADU > 0)*1
        AADU_kw = keyword_locate('ADU', text = data.comments) - not_AADU

        # entries containing "accessory dwelling" in the comments
        AADU_text = (keyword_locate('accessory dwelling', text = data.comments) -
                     keyword_locate('detached accessory dwelling', text = data.comments) > 0)*1
        AADU_kw_text = ((AADU_kw + AADU_text) > 0)*1

        SF = ((SF + AADU_kw_text) > 1)*1
    elif types == 'dadu':
        # entries containing "DADU"
        DADU_kw = keyword_locate('DADU', text = data.comments)

        # entries containing "detached accessory dwelling" in the comments
        DADU_text = keyword_locate('detached accessory dwelling', text = data.comments)
        DADU_kw_text = ((DADU_kw + DADU_text) > 0)*1

        SF = ((SF + DADU_kw_text) > 1)*1

    return pd.Series(SF.ravel())
