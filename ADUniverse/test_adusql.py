""" Tests for adusql """

import adusql
import numpy as np
import pandas as pd
import sqlite3
from common_data import app_data

SIZE = 5
TABLE = "new_table"
DATA = pd.DataFrame({
    'A': range(SIZE),
    'B': [2*v for v in range(SIZE)],
})
PIN = 9904000105


def test_constructor():
    conn = adusql.Connection()
    assert(not conn.connected)


def test_connect():
    conn = adusql.Connection()
    conn.connect()
    assert(conn.connected)


def test_createTable():
    conn = adusql.Connection()
    try:
        conn.createTable(DATA, TABLE)
    except:
        assert(False)
    conn.drop(TABLE)


def test_insert_select():
    conn = adusql.Connection()
    try:
        conn.createTable(DATA, TABLE)
        conn.insert(DATA, TABLE)
    except:
        assert(False)
    data = conn.select(TABLE)
    conn.drop(TABLE)
    assert(len(data) == 2*SIZE)


def test_drop():
    conn = adusql.Connection()
    conn.drop(TABLE)


def test_getFuncs():
    conn = adusql.Connection()
    for func in [conn.getParcelCoords,
                 conn.getZipcode]:
        data = func(PIN)
        assert(isinstance(data, pd.DataFrame))
        assert(len(data) > 0)


def test_getNeighbors():
    conn = adusql.Connection()
    df = conn.getParcelCoords(PIN)
    data = conn.getNeighbors(df)
    assert(isinstance(data, pd.DataFrame))
    assert(len(data) > 0)


def test_getAddresses():
    conn = adusql.Connection()
    data = conn.getAddresses()
    assert(isinstance(data, pd.DataFrame))
    assert(len(data) > 0)
