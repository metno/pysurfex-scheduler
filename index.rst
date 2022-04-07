.. pysurfex-scheduler Python API documentation master file, created by
   sphinx-quickstart on Mon Mar  2 18:25:38 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

PYSURFEX-scheduler documentation
=============================================

.. toctree::
   :maxdepth: 3
   :caption: Contents:

.. include::  README.rst
.. include::  docs/example.rst

Classes
---------------------------------------------
.. autoclass:: scheduler.SuiteDefinition
.. autoclass:: scheduler.EcflowNode
.. autoclass:: scheduler.EcflowNodeContainer
.. autoclass:: scheduler.EcflowSuite
.. autoclass:: scheduler.EcflowSuiteTriggers
.. autoclass:: scheduler.EcflowSuiteTrigger
.. autoclass:: scheduler.EcflowSuiteVariable
.. autoclass:: scheduler.EcflowSuiteFamily
.. autoclass:: scheduler.EcflowSuiteTask
.. autoclass:: scheduler.EcflowSubmitTask
.. autoclass:: scheduler.TaskSettings
.. autoclass:: scheduler.SubmitException
.. autoclass:: scheduler.KillException
.. autoclass:: scheduler.StatusException
.. autoclass:: scheduler.SubmissionBaseClass
.. autoclass:: scheduler.BackgroundSubmission
.. autoclass:: scheduler.BatchSubmission
.. autoclass:: scheduler.PBSSubmission
.. autoclass:: scheduler.SlurmSubmission
.. autoclass:: scheduler.GridEngineSubmission
.. autoclass:: scheduler.Server
.. autoclass:: scheduler.EcflowServer
.. autoclass:: scheduler.EcflowServerFromFile
.. autoclass:: scheduler.EcflowLogServer
.. autoclass:: scheduler.EcflowTask
.. autoclass:: scheduler.EcflowClient

Class methods
---------------------------------------------
.. autofunction:: scheduler.SuiteDefinition.__init__
.. autofunction:: scheduler.SuiteDefinition.save_as_defs
.. autofunction:: scheduler.EcflowNode.__init__
.. autofunction:: scheduler.EcflowNode.add_part_trigger
.. autofunction:: scheduler.EcflowNodeContainer.__init__
.. autofunction:: scheduler.EcflowSuite.__init__
.. autofunction:: scheduler.EcflowSuite.save_as_defs
.. autofunction:: scheduler.EcflowSuiteTriggers.__init__
.. autofunction:: scheduler.EcflowSuiteTriggers.create_string
.. autofunction:: scheduler.EcflowSuiteTriggers.add_triggers
.. autofunction:: scheduler.EcflowSuiteTrigger.__init__
.. autofunction:: scheduler.EcflowSuiteVariable.__init__
.. autofunction:: scheduler.EcflowSuiteFamily.__init__
.. autofunction:: scheduler.EcflowSuiteTask.__init__
.. autofunction:: scheduler.EcflowSubmitTask.write_header
.. autofunction:: scheduler.EcflowSubmitTask.write_trailer
.. autofunction:: scheduler.EcflowSubmitTask.write_job
.. autofunction:: scheduler.EcflowSubmitTask.submit
.. autofunction:: scheduler.TaskSettings.check_exceptions
.. autofunction:: scheduler.TaskSettings.process_settings
.. autofunction:: scheduler.TaskSettings.parse_submission_defs
.. autofunction:: scheduler.SubmitException.__init__
.. autofunction:: scheduler.KillException.__init__
.. autofunction:: scheduler.StatusException.__init__
.. autofunction:: scheduler.SubmissionBaseClass.update_db
.. autofunction:: scheduler.SubmissionBaseClass.clear_db
.. autofunction:: scheduler.SubmissionBaseClass.set_submit_cmd
.. autofunction:: scheduler.SubmissionBaseClass.set_jobid
.. autofunction:: scheduler.SubmissionBaseClass.get_logfile
.. autofunction:: scheduler.SubmissionBaseClass.submit_job
.. autofunction:: scheduler.SubmissionBaseClass.kill_job
.. autofunction:: scheduler.SubmissionBaseClass.set_job_status
.. autofunction:: scheduler.SubmissionBaseClass.status
.. autofunction:: scheduler.SubmissionBaseClass.job_status
.. autofunction:: scheduler.SubmissionBaseClass.kill
.. autofunction:: scheduler.SubmissionBaseClass.set_kill_cmd
.. autofunction:: scheduler.SubmissionBaseClass.set_remote_cmd
.. autofunction:: scheduler.SubmissionBaseClass.set_output
.. autofunction:: scheduler.SubmissionBaseClass.set_job_name
.. autofunction:: scheduler.BackgroundSubmission.__init__
.. autofunction:: scheduler.BackgroundSubmission.set_submit_cmd
.. autofunction:: scheduler.BackgroundSubmission.set_jobid
.. autofunction:: scheduler.BackgroundSubmission.get_logfile
.. autofunction:: scheduler.BackgroundSubmission.set_kill_cmd
.. autofunction:: scheduler.BackgroundSubmission.set_job_status
.. autofunction:: scheduler.BackgroundSubmission.set_output
.. autofunction:: scheduler.BackgroundSubmission.set_job_name
.. autofunction:: scheduler.BatchSubmission.__init__
.. autofunction:: scheduler.BatchSubmission.set_submit_cmd
.. autofunction:: scheduler.BatchSubmission.set_jobid
.. autofunction:: scheduler.BatchSubmission.get_logfile
.. autofunction:: scheduler.BatchSubmission.set_kill_cmd
.. autofunction:: scheduler.BatchSubmission.set_job_status
.. autofunction:: scheduler.BatchSubmission.set_output
.. autofunction:: scheduler.BatchSubmission.set_job_name
.. autofunction:: scheduler.PBSSubmission.__init__
.. autofunction:: scheduler.PBSSubmission.set_jobid
.. autofunction:: scheduler.PBSSubmission.set_job_name
.. autofunction:: scheduler.SlurmSubmission.__init__
.. autofunction:: scheduler.SlurmSubmission.set_output
.. autofunction:: scheduler.SlurmSubmission.set_jobid
.. autofunction:: scheduler.SlurmSubmission.set_job_name
.. autofunction:: scheduler.GridEngineSubmission.__init__
.. autofunction:: scheduler.GridEngineSubmission.set_output
.. autofunction:: scheduler.GridEngineSubmission.set_jobid
.. autofunction:: scheduler.GridEngineSubmission.set_job_name
.. autofunction:: scheduler.Server.__init__
.. autofunction:: scheduler.Server.start_server
.. autofunction:: scheduler.Server.replace
.. autofunction:: scheduler.Server.start_suite
.. autofunction:: scheduler.EcflowServer.__init__
.. autofunction:: scheduler.EcflowServer.start_server
.. autofunction:: scheduler.EcflowServer.force_complete
.. autofunction:: scheduler.EcflowServer.force_aborted
.. autofunction:: scheduler.EcflowServer.update_submission_id
.. autofunction:: scheduler.EcflowServer.replace
.. autofunction:: scheduler.EcflowServer.update_log
.. autofunction:: scheduler.EcflowServerFromFile.__init__
.. autofunction:: scheduler.EcflowServerFromFile.get_var
.. autofunction:: scheduler.EcflowServerFromFile.save_as_file
.. autofunction:: scheduler.EcflowServerFromFile.get_file_name
.. autofunction:: scheduler.EcflowLogServer.__init__
.. autofunction:: scheduler.EcflowTask.__init__
.. autofunction:: scheduler.EcflowTask.create_submission_log
.. autofunction:: scheduler.EcflowTask.create_kill_log
.. autofunction:: scheduler.EcflowTask.create_status_log
.. autofunction:: scheduler.EcflowTask.create_ecf_job
.. autofunction:: scheduler.EcflowTask.create_ecf_jobout
.. autofunction:: scheduler.EcflowClient.__init__
.. autofunction:: scheduler.EcflowClient.at_time
.. autofunction:: scheduler.EcflowClient.signal_handler
.. autofunction:: scheduler.EcflowClient.__enter__
.. autofunction:: scheduler.EcflowClient.__exit__

Methods
---------------------------------------------
.. autofunction:: scheduler.parse_submit_cmd
.. autofunction:: scheduler.submit_cmd
.. autofunction:: scheduler.parse_kill_cmd
.. autofunction:: scheduler.kill_cmd
.. autofunction:: scheduler.parse_status_cmd
.. autofunction:: scheduler.status_cmd
.. autofunction:: scheduler.get_submission_object


* :ref: `README`

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


