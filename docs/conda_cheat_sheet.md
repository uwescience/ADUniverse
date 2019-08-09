# Conda Cheat Sheet

Note that these commands apply **only to the terminal session in
which they are issued**. So, if you want to use multiple terminal sessions, you must make sure that each is in the same virtual environment.

- Create an empty environment (just python)
  - ``conda create --name <name of enviornment> python=3.6``

- Add sourceforge channel to look for packages
  - ``conda config --add channels conda-forge``

- List environments
  - ``conda env list``
  - The environment with an asterik is your current environment

- Activate an environment
  - ``conda activate <name of environment>``

- List packages in environment
  - ``conda list --name <name of environment>``

- Install packages
  - ``conda install -n <name of environment> <package>``
  - Some packages may not be found by your conda channels. You
should do a google search ``conda install <package name>`` to
find out how to do it. For example, google maps is installed
using ``conda install -c conda-forge googlemaps``. You can set
to the conda-forge channel as above.
  - To install from ``requirements.txt``, use ``conda install --yes --file requirements.txt``

- Deactivate environment
  - ``conda deactivate``

- Remove an environment
  - ``conda env remove -name <name of environment>``

