![](https://travis-ci.org/uwescience/ADUniverse.svg?branch=master)

# ADUniverse

Auxiliary Dwelling Units (ADU) such as backyard cottages and in-house mother-in-law apartments provide a way for the City of Seattle to address housing affordability. This project is about aiding owners of single family homes to assess the eligibility and desirability of building an ADU. We illustrate our vision via a prototype software tool for homeowners. Further details are provided in a white paper.

See [project web page](https://uwescience.github.io/ADUniverse/).

By using the dataset (adunits.db) from this repository, you agree to the City of Seattle's [Terms of Use and Policy](https://data.seattle.gov/stories/s/Data-Policy/6ukr-wvup/), as well as to the [King County Assessors'](https://info.kingcounty.gov/assessor/DataDownload/default.aspx), the US Census Bureau's and Zillow's, from whom this data was acquired. 

## Installation
First, clone this repository by using ``git clone``.
This code works for python 3.6. You have have miniconda installed. Then issue the following commands:
- ``pip install -U googlemaps``
- ``pip install dash folium nltk dash_daq``
- ``pip install dash_bootstrap_components``

To run the code, change to the ```ADUniverse`` directory and the ``ADUniverse`` subdirectory within the first directory. Then, run the command ``python index.py``.

