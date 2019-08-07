#!/bin/bash
pip install -U googlemaps
pip install dash folium nltk dash_daq
sudo apt-get install curl
curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash
git lfs install
