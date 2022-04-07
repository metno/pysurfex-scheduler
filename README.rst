.. _README:

.. image:: https://coveralls.io/repos/github/metno/pysurfex-scheduler/badge.svg?branch=master

https://coveralls.io/github/metno/pysurfex-scheduler

Python abstraction layer for a scheduling system like Ecflow
================================================================

See online documentation in https://metno.github.io/pysurfex-scheduler/

Installation of pregenerated packages from pypi (pip)
---------------------------------------------------------

.. code-block:: bash

    pip3 install pysurfex-scheduler

User installation:

.. code-block:: bash

    pip3 install pysurfex-scheduler --user


Installation on debian based Linux system
--------------------------------------------

Install the required pacakges (some might be obsolete if the pip packages contain the needed depedencies):

.. code-block:: bash

  sudo apt-get update
  # Python tools
  sudo apt-get install python3-setuptools
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

.. code-block:: bash

  sudo pip3 install -e .

or

.. code-block:: bash

  pip3 install -e . --user

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


Usage
--------------------

.. code-block:: python

 import scheduler
 
 # EcFlow variables parsed in EcFlow job
 ecf_name = "%ECF_NAME%"
 ecf_pass = "%ECF_PASS%"
 ecf_tryno = "%ECF_TRYNO%"
 ecf_rid = "%ECF_RID%"
 submission_id = "%SUBMISSION_ID%"
 task_name = "%TASK%"
 
 task = scheduler.EcflowTask(ecf_name, ecf_tryno, ecf_pass, ecf_rid, submission_id)
 env_submit = {}
 env_server = {
   "ECF_HOST": "localhost",
   "ECF_PORT": 3141,
   "ECF_PORT_OFFSET": 0
 }
 joboutdir = "/tmp/job"
 
 sub = scheduler.EcflowSubmitTask(task, env_submit, env_server, joboutdir)
 sub.submit()
