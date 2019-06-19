"""
Creates a table in the aduniverse.db file.
"""

import numpy as np
import os
import pandas as pd
import sqlite3 as sql
from sqlalchemy import create_engine

DATA_PATH = "data"
DBNAME = "aduniverse.db"

def main(csv_file, tablename=None):
  file_path = os.path.join(DATA_PATH, csv_file)
  db_path = os.path.join(DATA_PATH, DBNAME)
  try:
    conn = sql.connect(db_path)
  except:
    raise ValueError("Cannot connect to DataBase %s" % DBNAME)
  df = pd.read_csv(file_path, low_memory=False)
  if tablename is None:
    splits = csv_file.split(".")
    if len(splits) != 2:
      raise ValueError("Invalid CSV file name: %s" % csv_file)
    tablename = splits[0]
  df.to_sql(tablename, conn, index=False, if_exists="replace")
  dff = pd.read_sql_query("SELECT * from %s" % tablename, conn)
  conn.close()

  
if __name__ == '__main__':
  main("Residential_Building_Permits__Issued_and_Final.csv",
      "permits")  
