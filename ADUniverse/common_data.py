'''Data Used across modules.'''

import pandas as pd


class AppData(object):
    def __init__(self):
        self.zipcode = 98115
        self.parcel_coords = None
        self.neighbor = pd.DataFrame()


app_data = AppData()
