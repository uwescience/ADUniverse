# Conda Cheat Sheet

- Create an empty environment (just python)
  - ``conda create --name <name of enviornment> python=3.6``

- List environments
  - ``conda env list``
  - The environment with an asterik is your current environment

- Activate an environment
  - ``activate <name of environment>``

- List packages in environment
  - ``conda list --name <name of environment>``

- Deactivate environment
  - ``deactivate``
  - Note that this gives a deprecation warning

- Remove an environment
  - ``conda env remove -name <name of environment>``

