# Conda Cheat Sheet

- Create an empty environment (just python)
  - ``conda create --name <name of enviornment> python=3.6``

- List environments
  - ``conda env list``
  - The environment with an asterik is your current environment

- Activate an environment
  - ``conda activate <name of environment>``

- List packages in environment
  - ``conda list --name <name of environment>``

- Install packages
  - ``conda install -n <name of environment> <package>``

- Deactivate environment
  - ``conda deactivate``
  - Note that this gives a deprecation warning

- Remove an environment
  - ``conda env remove -name <name of environment>``

