"""
Creates a table in the aduniverse.db file.
"""

import argparse
import numpy as np
import os
import pandas as pd
import sqlite3 as sql
from sqlalchemy import create_engine

DATA_PATH = "data"
DBNAME = "aduniverse.db"

def main(csv_file, tablename=None):
  """
  :param str csv_file: file in data directory with extension
  :parm str tablename:
  """
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
  description = "Put CSV file into a SQL DB"
  parser = argparse.ArgumentParser(description=description)
  parser.add_argument('csv_file', type=str, help='CSV file')
  parser.add_argument('table_name', type=str, 
      help='Name of database table')
  args = parser.parse_args()
  main(args.csv_file, tablename=args.table_name)
