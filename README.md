![](https://travis-ci.org/uwescience/ADUniverse.svg?branch=master)

# ADUniverse

Auxiliary Dwelling Units (ADU) such as backyard cottages and in-house mother-in-law apartments provide a way for the City of Seattle to address housing affordability. This project is about aiding owners of single family homes to assess the eligibility and desirability of building an ADU. We illustrate our vision via a prototype software tool for homeowners. Further details are provided in a white paper.

See [project web page](https://uwescience.github.io/ADUniverse/).

By using the dataset (adunits.db) from this repository, you agree to the City of Seattle's [Terms of Use and Policy](https://data.seattle.gov/stories/s/Data-Policy/6ukr-wvup/), as well as to the [King County Assessors'](https://info.kingcounty.gov/assessor/DataDownload/default.aspx), the US Census Bureau's and Zillow's, from whom this data was acquired. 

## Installation
Your machione should have the following installed already:
- python 3
- [miniconda for python 3](https://docs.conda.io/en/latest/miniconda.html)
- [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

First, clone ADU repository repository by using ``git clone https://github.com/uwescience/ADUniverse``.

You will be working in a "virtual environment".
- ``conda create -n test_adu python=3.6``
- ``conda activate test_adu``

This code works for python 3.6. You should have miniconda installed. Then issue the following commands:
- ``conda install -f -y -q --name test_adu -c conda-forge --file requirements.txt``

You just installed all the necessary dependencies needed but LFS (large file system). Now let's install lfs with the following commands:
- ``git lfs install``

Clone again to include the large database by using ``git clone https://github.com/uwescience/ADUniverse``

To run the code, change to the ``ADUniverse`` directory and the ``ADUniverse`` subdirectory within the first directory. Then, run the command ``python index.py``.

When you are done,
- ``conda deactivate``
