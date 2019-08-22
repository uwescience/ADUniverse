import update_map
import pandas as pd
import adusql as ads


def test_update_map():
    PIN = 3626039263
    adunit = ads.Connection("adunits.db")
    df = adunit.getParcelCoords(PIN)
    neighbors = adunit.getNeighbors(df)
    result = update_map.update_map(df, neighbors)
    assert(isinstance(result, object))
