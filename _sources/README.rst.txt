.. _README:

.. image:: https://coveralls.io/repos/github/metno/pysurfex-scheduler/badge.svg?branch=master

https://coveralls.io/github/metno/pysurfex-scheduler

Python abstraction layer for a scheduling system like Ecflow
================================================================

See online documentation in https://metno.github.io/pysurfex-scheduler/

Installation of pregenerated packages from pypi (pip)
---------------------------------------------------------

.. code-block:: bash

    pip3 install pysurfex-scheduler --use-feature=2020-resolver

User installation:

.. code-block:: bash

    pip3 install pysurfex-scheduler --user --use-feature=2020-resolver


Installation on debian based Linux system
--------------------------------------------

Install the required pacakges (some might be obsolete if the pip packages contain the needed depedencies):

.. code-block:: bash

  sudo apt-get update
  # Python tools
  sudo apt-get install python3-setuptools python3-numpy python3-scipy python3-nose
  # Ecflow
  sudo apt-get install ecflow-server ecflow-client python3-ecflow

The following depencies are needed. Install the non-standard ones e.g. with pip or your system installation system.

General dependencies (from pypi)
---------------------------------

.. code-block:: bash

  toml
  json; python_version < '3'

For testing:

.. code-block:: bash

  unittest
  nose

Download the source code, then install ``pysurfex-scheduler`` by executing the following inside the extracted
folder:

Install pysurfex
-------------------------------------------
.. code-block:: bash

  sudo pip install -e .

or

.. code-block:: bash

  sudo pip install -e . --user

Create documentation
---------------------------------------------

.. code-block:: bash

  cd docs
  # Create html documentation
  make html
  # Create latex documentation
  make latex
  # Create a pdf documentation
  make latexpdf


Examples
-----------------------

See https://metno.github.io/pysurfex-scheduler/#examples
