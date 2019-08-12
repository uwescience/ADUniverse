# create the virtual environment
conda create -q -n test-environment python=3.6
source activate test-environment

# clone the repository
mkdir /Users/NiuYuanhao/documents/test
git clone https://github.com/uwescience/ADUniverse
cd /Users/NiuYuanhao/documents/test/ADUniverse

# get linux and conda
# sudo apt-get update  # get most recent installer for linux
# wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh # downloading miniconda
# bash miniconda.sh -b -p $HOME/miniconda   # install miniconda
# export PATH="$HOME/miniconda/bin:$PATH"   # setup miniconda to the path
# hash -r
# conda config --set always_yes yes --set changeps1 no  # config conda
# conda update --quiet conda    # kill message
# conda info --all       # yield info

# Install dependencies

conda install -f -y -q --name test-environment -c conda-forge --file requirements.txt

# Install support for large files
# sudo apt-get install curl
# curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash
# git lfs install
