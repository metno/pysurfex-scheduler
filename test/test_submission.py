import unittest
import scheduler
import os


class TestSubmit(unittest.TestCase):

    @staticmethod
    def test_submission():

        joboutdirs = {
            "0": "/tmp/host0/job",
            "1": "/tmp/host1/job"
        }
        env_file = "/tmp/host1/Env"
        fh = open(env_file, "w")
        fh.write("print(\"Oh my environment\n\")")
        fh.close()

        os.makedirs("/tmp/host1/job/test_submission/Forecasting/", exist_ok=True)
        job_file = "/tmp/host1/job/test_submission/Forecasting/Forecast.job1"
        fh = open(job_file, "w")
        fh.write("host = \"@HOST_TO_BE_SUBSTITUTED@\"")
        fh.write("wrapper = \"@WRAPPER_TO_BE_SUBSTITUTED@\"")
        fh.close()

        ecf_name = "/test_submission/Forecasting/Forecast"
        ecf_tryno = 1
        ecf_pass = "dummy_password"

        task = scheduler.EcflowTask(ecf_name, ecf_tryno, ecf_pass, ecf_rid=int(os.getpid()),
                                    submission_id=None)

        exceptions = {
            "complete": {
                "task": {
                    "Forecast": "is_coldstart"
                },
                "family": {
                    "Forecasting": "is_coldstart"
                }
            }
        }

        env_submit = {
            "submit_types": ["background", "scalar"],
            "default_submit_type": "scalar",
            "background": {
                "HOST": "0",
                "OMP_NUM_THREADS": "import os\nos.environ.update({\"OMP_NUM_THREADS\": \"1\"})",
                "tasks": [
                    "InitRun",
                    "LogProgress",
                    "LogProgressPP"
                ]
            },
            "scalar": {
                "HOST": "1",
                "SUBMIT_TYPE": "slurm",
                "SSH": "ssh " + os.environ["USER"] + "@localhost",
                "INTERPRETER": "#!/usr/bin/env python3",
                "WRAPPER": "wrapper",
                "Not_existing_task": {
                    "DR_HOOK": "print(\"hei\")"
                }
            }
        }

        ecf_host = "localhost"
        ecf_port = (int(os.getuid()) + 1500)
        logfile = "unittest_ECF.log"
        server = scheduler.EcflowServer(ecf_host, ecf_port, logfile)

        submit = scheduler.EcflowSubmitTask(task, env_submit, server, joboutdirs,
                                            submit_exceptions=exceptions, env_file=env_file)
        submit.write_job()

    def test_slurm(self):

        exp = "test_slurm"
        ecf_name = "/" + exp + "/Forecasting/Forecast"
        ecf_tryno = 1
        ecf_pass = "dummy_password"

        task = scheduler.EcflowTask(ecf_name, ecf_tryno, ecf_pass, ecf_rid=int(os.getpid()),
                                    submission_id=None)
        os.makedirs("/tmp/host1/job/" + exp + "/Forecasting/", exist_ok=True)
        fh = open("/tmp/host1/job/" + exp + "/Forecasting/Forecast.job1", "w")
        fh.write("My job generated by ecflow")
        fh.close()

        joboutdirs = {
            "0": "/tmp/host0/job/",
            "1": "/tmp/host1/job/"
        }

        env_submit = {
            "submit_types": ["background", "scalar"],
            "default_submit_type": "scalar",
            "background": {
                "HOST": "0",
                "OMP_NUM_THREADS": "import os\nos.environ.update({\"OMP_NUM_THREADS\": \"1\"})",
                "tasks": [
                    "InitRun",
                    "LogProgress",
                    "LogProgressPP"
                ]
            },
            "scalar": {
                "HOST": "1",
                "SUBMIT_TYPE": "slurm",
                "SSH": "ssh " + os.environ["USER"] + "@localhost",
                "INTERPRETER": "#!/usr/bin/env python3",
                "WRAPPER": "wrapper",
                "Not_existing_task": {
                    "DR_HOOK": "print(\"hei\")"
                }
            }
        }

        task_settings = scheduler.TaskSettings(task, env_submit, joboutdirs)
        sub = scheduler.SlurmSubmission(task, task_settings, sub=os.getcwd() + "/test/bin/sbatch")
        sub.set_submit_cmd()
        sub.submit_job()
        sub.set_jobid()
        self.assertEqual(sub.job_id, "slurm.12345")
        if not os.path.exists("/tmp/host1/job/" + exp + "/Forecasting/Forecast.job1.sub"):
            raise Exception("Expected sub file mot found")

        task = scheduler.EcflowTask(ecf_name, ecf_tryno, ecf_pass, ecf_rid=int(os.getpid()),
                                    submission_id=sub.job_id)
        sub = scheduler.get_submission_object(task, task_settings)
        sub.status()
        if not os.path.exists("/tmp/host1/job/" + exp + "/Forecasting/Forecast.job1.stat"):
            raise Exception("Expected status file mot found")
        sub.kill()
        if not os.path.exists("/tmp/host1/job/" + exp + "/Forecasting/Forecast.job1.kill"):
            raise Exception("Expected kill file mot found")

    def test_pbs(self):
        exp = "test_pbs"

        ecf_name = "/" + exp + "/Forecasting/Forecast"
        ecf_tryno = 1
        ecf_pass = "dummy_password"

        task = scheduler.EcflowTask(ecf_name, ecf_tryno, ecf_pass, ecf_rid=int(os.getpid()),
                                    submission_id=None)
        os.makedirs("/tmp/host1/job/" + exp + "/Forecasting/", exist_ok=True)
        fh = open("/tmp/host1/job/" + exp + "/Forecasting/Forecast.job1", "w")
        fh.write("My job generated by ecflow")
        fh.close()

        joboutdirs = {
            "0": "/tmp/host0/job/",
            "1": "/tmp/host1/job/"
        }

        env_submit = {
            "submit_types": ["background", "scalar"],
            "default_submit_type": "scalar",
            "background": {
                "HOST": "0",
                "OMP_NUM_THREADS": "import os\nos.environ.update({\"OMP_NUM_THREADS\": \"1\"})",
                "tasks": [
                    "InitRun",
                    "LogProgress",
                    "LogProgressPP"
                ]
            },
            "scalar": {
                "HOST": "1",
                "SUBMIT_TYPE": "pbs",
                "Not_existing_task": {
                    "DR_HOOK": "print(\"hei\")"
                }
            }
        }

        task_settings = scheduler.TaskSettings(task, env_submit, joboutdirs)
        sub = scheduler.get_submission_object(task, task_settings)
        sub.set_submit_cmd()
        sub.submit_job()
        sub.set_jobid()
        self.assertEqual(sub.job_id, "pbs.12345")
        if not os.path.exists("/tmp/host1/job/" + exp + "/Forecasting/Forecast.job1.sub"):
            raise Exception("Expected sub file mot found")

        task = scheduler.EcflowTask(ecf_name, ecf_tryno, ecf_pass, ecf_rid=int(os.getpid()),
                                    submission_id=sub.job_id)
        sub = scheduler.PBSSubmission(task, task_settings)
        sub.status()
        if not os.path.exists("/tmp/host1/job/" + exp + "/Forecasting/Forecast.job1.stat"):
            raise Exception("Expected status file mot found")
        sub.kill()
        if not os.path.exists("/tmp/host1/job/" + exp + "/Forecasting/Forecast.job1.kill"):
            raise Exception("Expected kill file mot found")

    def test_grid_engine(self):
        exp = "test_grid_engine"

        ecf_name = "/" + exp + "/Forecasting/Forecast"
        ecf_tryno = 1
        ecf_pass = "dummy_password"

        task = scheduler.EcflowTask(ecf_name, ecf_tryno, ecf_pass, ecf_rid=int(os.getpid()),
                                    submission_id=None)
        os.makedirs("/tmp/host1/job/" + exp + "/Forecasting/", exist_ok=True)
        fh = open("/tmp/host1/job/" + exp + "/Forecasting/Forecast.job1", "w")
        fh.write("My job generated by ecflow")
        fh.close()

        joboutdirs = {
            "0": "/tmp/host0/job/",
            "1": "/tmp/host1/job/"
        }

        env_submit = {
            "submit_types": ["background", "scalar"],
            "default_submit_type": "scalar",
            "background": {
                "HOST": "0",
                "OMP_NUM_THREADS": "import os\nos.environ.update({\"OMP_NUM_THREADS\": \"1\"})",
                "tasks": [
                    "InitRun",
                    "LogProgress",
                    "LogProgressPP"
                ]
            },
            "scalar": {
                "HOST": "1",
                "SUBMIT_TYPE": "grid_engine",
                "SUBMIT": "qsub_sge",
                "Not_existing_task": {
                    "DR_HOOK": "print(\"hei\")"
                }
            }
        }

        task_settings = scheduler.TaskSettings(task, env_submit, joboutdirs)
        # Test default
        scheduler.get_submission_object(task, task_settings)
        # Make my own test SGE
        sub = scheduler.GridEngineSubmission(task, task_settings, sub="qsub_sge", stat="qstat_sge -j", kill="qdel_sge")
        sub.set_submit_cmd()
        sub.submit_job()
        sub.set_jobid()
        self.assertEqual(sub.job_id, "sge.12345")
        if not os.path.exists("/tmp/host1/job/" + exp + "/Forecasting/Forecast.job1.sub"):
            raise Exception("Expected sub file mot found")

        task = scheduler.EcflowTask(ecf_name, ecf_tryno, ecf_pass, ecf_rid=int(os.getpid()),
                                    submission_id=sub.job_id)
        sub = scheduler.GridEngineSubmission(task, task_settings, sub="qsub_sge", stat="qstat_sge -j", kill="qdel_sge")
        sub.status()
        if not os.path.exists("/tmp/host1/job/" + exp + "/Forecasting/Forecast.job1.stat"):
            raise Exception("Expected status file mot found")
        sub.kill()
        if not os.path.exists("/tmp/host1/job/" + exp + "/Forecasting/Forecast.job1.kill"):
            raise Exception("Expected kill file mot found")