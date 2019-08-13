'''Data Used across modules.'''

import pandas as pd


class AppData(object):
    def __init__(self):
        self.zipcode = 0
        self.parcel_coords = None
        self.neighbor = pd.DataFrame()


app_data = AppData()
