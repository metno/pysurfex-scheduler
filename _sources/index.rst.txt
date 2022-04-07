.. pysurfex-scheduler Python API documentation master file, created by
   sphinx-quickstart on Mon Mar  2 18:25:38 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

PYSURFEX scheduler documentation
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
.. automethod:: scheduler.SuiteDefinition.__init__
.. automethod:: scheduler.SuiteDefinition.save_as_defs
.. automethod:: scheduler.EcflowNode.__init__
.. automethod:: scheduler.EcflowNode.add_part_trigger
.. automethod:: scheduler.EcflowNodeContainer.__init__
.. automethod:: scheduler.EcflowSuite.__init__
.. automethod:: scheduler.EcflowSuite.save_as_defs
.. automethod:: scheduler.EcflowSuiteTriggers.__init__
.. automethod:: scheduler.EcflowSuiteTriggers.create_string
.. automethod:: scheduler.EcflowSuiteTriggers.add_triggers
.. automethod:: scheduler.EcflowSuiteTrigger.__init__
.. automethod:: scheduler.EcflowSuiteVariable.__init__
.. automethod:: scheduler.EcflowSuiteFamily.__init__
.. automethod:: scheduler.EcflowSuiteTask.__init__
.. automethod:: scheduler.EcflowSubmitTask.write_header
.. automethod:: scheduler.EcflowSubmitTask.write_trailer
.. automethod:: scheduler.EcflowSubmitTask.write_job
.. automethod:: scheduler.EcflowSubmitTask.submit
.. automethod:: scheduler.TaskSettings.check_exceptions
.. automethod:: scheduler.TaskSettings.process_settings
.. automethod:: scheduler.TaskSettings.parse_submission_defs
.. automethod:: scheduler.SubmitException.__init__
.. automethod:: scheduler.KillException.__init__
.. automethod:: scheduler.StatusException.__init__
.. automethod:: scheduler.SubmissionBaseClass.update_db
.. automethod:: scheduler.SubmissionBaseClass.clear_db
.. automethod:: scheduler.SubmissionBaseClass.set_submit_cmd
.. automethod:: scheduler.SubmissionBaseClass.set_jobid
.. automethod:: scheduler.SubmissionBaseClass.get_logfile
.. automethod:: scheduler.SubmissionBaseClass.submit_job
.. automethod:: scheduler.SubmissionBaseClass.kill_job
.. automethod:: scheduler.SubmissionBaseClass.set_job_status
.. automethod:: scheduler.SubmissionBaseClass.status
.. automethod:: scheduler.SubmissionBaseClass.job_status
.. automethod:: scheduler.SubmissionBaseClass.kill
.. automethod:: scheduler.SubmissionBaseClass.set_kill_cmd
.. automethod:: scheduler.SubmissionBaseClass.set_remote_cmd
.. automethod:: scheduler.SubmissionBaseClass.set_output
.. automethod:: scheduler.SubmissionBaseClass.set_job_name
.. automethod:: scheduler.BackgroundSubmission.__init__
.. automethod:: scheduler.BackgroundSubmission.set_submit_cmd
.. automethod:: scheduler.BackgroundSubmission.set_jobid
.. automethod:: scheduler.BackgroundSubmission.get_logfile
.. automethod:: scheduler.BackgroundSubmission.set_kill_cmd
.. automethod:: scheduler.BackgroundSubmission.set_job_status
.. automethod:: scheduler.BackgroundSubmission.set_output
.. automethod:: scheduler.BackgroundSubmission.set_job_name
.. automethod:: scheduler.BatchSubmission.__init__
.. automethod:: scheduler.BatchSubmission.set_submit_cmd
.. automethod:: scheduler.BatchSubmission.set_jobid
.. automethod:: scheduler.BatchSubmission.get_logfile
.. automethod:: scheduler.BatchSubmission.set_kill_cmd
.. automethod:: scheduler.BatchSubmission.set_job_status
.. automethod:: scheduler.BatchSubmission.set_output
.. automethod:: scheduler.BatchSubmission.set_job_name
.. automethod:: scheduler.PBSSubmission.__init__
.. automethod:: scheduler.PBSSubmission.set_jobid
.. automethod:: scheduler.PBSSubmission.set_job_name
.. automethod:: scheduler.SlurmSubmission.__init__
.. automethod:: scheduler.SlurmSubmission.set_output
.. automethod:: scheduler.SlurmSubmission.set_jobid
.. automethod:: scheduler.SlurmSubmission.set_job_name
.. automethod:: scheduler.GridEngineSubmission.__init__
.. automethod:: scheduler.GridEngineSubmission.set_output
.. automethod:: scheduler.GridEngineSubmission.set_jobid
.. automethod:: scheduler.GridEngineSubmission.set_job_name
.. automethod:: scheduler.Server.__init__
.. automethod:: scheduler.Server.start_server
.. automethod:: scheduler.Server.replace
.. automethod:: scheduler.Server.start_suite
.. automethod:: scheduler.EcflowServer.__init__
.. automethod:: scheduler.EcflowServer.start_server
.. automethod:: scheduler.EcflowServer.force_complete
.. automethod:: scheduler.EcflowServer.force_aborted
.. automethod:: scheduler.EcflowServer.update_submission_id
.. automethod:: scheduler.EcflowServer.replace
.. automethod:: scheduler.EcflowServer.update_log
.. automethod:: scheduler.EcflowServerFromFile.__init__
.. automethod:: scheduler.EcflowServerFromFile.get_var
.. automethod:: scheduler.EcflowServerFromFile.save_as_file
.. automethod:: scheduler.EcflowServerFromFile.get_file_name
.. automethod:: scheduler.EcflowLogServer.__init__
.. automethod:: scheduler.EcflowTask.__init__
.. automethod:: scheduler.EcflowTask.create_submission_log
.. automethod:: scheduler.EcflowTask.create_kill_log
.. automethod:: scheduler.EcflowTask.create_status_log
.. automethod:: scheduler.EcflowTask.create_ecf_job
.. automethod:: scheduler.EcflowTask.create_ecf_jobout
.. automethod:: scheduler.EcflowClient.__init__
.. automethod:: scheduler.EcflowClient.at_time
.. automethod:: scheduler.EcflowClient.signal_handler
.. automethod:: scheduler.EcflowClient.__enter__
.. automethod:: scheduler.EcflowClient.__exit__

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
* :ref:`search`


