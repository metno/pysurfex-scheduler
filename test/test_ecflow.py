import unittest
import scheduler
import os
import json
import toml


class EcflowTest(unittest.TestCase):

    @staticmethod
    def test_suite():
        suite_name = "test_suite"
        def_file = "test_suite.def"
        joboutdir = "/tmp/host1/job/"
        exp_dir = "/tmp/host1/" + suite_name
        os.makedirs(exp_dir, exist_ok=True)
        ecf_files = exp_dir + "/ecf/"
        os.makedirs(ecf_files, exist_ok=True)
        fh = open(ecf_files + "/default.py", "w")
        fh.write("print(\"Default python task\")")
        fh.close()
        env_submit_file = exp_dir + "/env_submit.json"
        env_submit = {
            "submit_types": ["background"],
            "default_submit_type": "scalar",
            "background": {
                "HOST": "0",
                "tasks": [
                ]
            }
        }
        json.dump(env_submit, open(env_submit_file, "w"))
        server_config_file = exp_dir + "/env_server.toml"
        server_config = {
            "ECF_HOST": "localhost"
        }
        toml.dump(server_config, open(server_config_file, "w"))
        server_log = exp_dir + "/ECF.log"
        defs = scheduler.SuiteDefinition(suite_name, def_file, joboutdir, ecf_files, env_submit_file,
                                         server_config_file, server_log)
        defs.suite.ecf_node.add_variable("DTG", "YYYYMMDDHH")
        task1 = scheduler.EcflowSuiteTask("My_task1", defs.suite, ecf_files=ecf_files)
        trigger = scheduler.EcflowSuiteTriggers(scheduler.EcflowSuiteTrigger(task1, "complete"))
        scheduler.EcflowSuiteTask("My_task2", defs.suite, ecf_files=ecf_files, triggers=trigger)

    @staticmethod
    def test_client():
        exp = "test_client"

        joboutdir = "/tmp/host1/job/"
        os.makedirs(joboutdir, exist_ok=True)
        env_submit_file = "/tmp/host1/env_submit_file.json"
        env_server_file = "/tmp/host1/env_submit_file.toml"
        env_submit = {
            "submit_types": ["background"],
            "default_submit_type": "background",
            "background": {
                "HOST": "0"
            }
        }
        json.dump(env_submit, open(env_submit_file, "w"))
        toml.dump({"ECF_HOST": "localhost"}, open(env_server_file, "w"))
        # Dry submit
        argv = [
            "-sub", env_submit_file,
            "-dir", joboutdir,
            "-server", env_server_file,
            "--log", "logfile",
            "-ecf_name", exp + "/dry_submit",
            "-ecf_pass", "12345",
            "-ecf_tryno", "1"
        ]
        print(argv)
        kwargs = scheduler.parse_submit_cmd(argv, exp=False)
        kwargs.update({"dry_run": True})
        scheduler.submit_cmd(**kwargs)

        # Dry status
        argv = [
            "-dir", joboutdir,
            "-sub", env_submit_file,
            "-ecf_name", exp + "/dry_submit",
            "-ecf_pass", "12345",
            "-ecf_tryno", "1",
            "-submission_id", "0"
        ]
        print(argv)
        kwargs = scheduler.parse_status_cmd(argv, exp=False)
        kwargs.update({"dry_run": True})
        scheduler.status_cmd(**kwargs)

        # Dry Kill
        argv = [
            "-sub", env_submit_file,
            "-server", env_server_file,
            "--log", "logfile",
            "-dir", joboutdir,
            "-ecf_name", exp + "/dry_submit",
            "-ecf_pass", "12345",
            "-ecf_tryno", "1",
            "-submission_id", "0"
        ]
        print(argv)
        kwargs = scheduler.parse_kill_cmd(argv, exp=False)
        kwargs.update({"dry_run": True})
        scheduler.kill_cmd(**kwargs)

    @staticmethod
    def test_ecflow_client():

        ecf_host = "localhost"
        ecf_port = (int(os.getuid()) + 1500)
        logfile = "unittest_ECF.log"
        server = scheduler.EcflowServer(ecf_host, ecf_port, logfile)

        def_file = "unittest_test_ecflow.def"
        suite_name = "test_ecflow"
        suite = scheduler.EcflowSuite(suite_name, def_file=def_file)
        fam = scheduler.EcflowSuiteFamily("My_family", suite)
        var = scheduler.EcflowSuiteVariable("ECF_PASS", "FREE")
        scheduler.EcflowSuiteTask("My_task", fam, variables=var)

        suite.save_as_defs()
        server.start_server()
        server.replace(suite_name, def_file)
        server.begin_suite(suite_name)

        # Typically inside ecflow task job file e.g. default.py
        ecf_name = "/test_ecflow/My_family/My_task"
        ecf_pass = "FREE"
        ecf_tryno = "1"
        task = scheduler.EcflowTask(ecf_name, ecf_tryno, ecf_pass, ecf_rid=None)

        with scheduler.EcflowClient(server, task) as ci:
            print("Running task ")
            task.submission_id = "test.12345"
            server.update_submission_id(task)
            server.update_log("Hello log")

    def test_ecflow_client_failed(self):

        ecf_host = "localhost"
        ecf_port = (int(os.getuid()) + 1500)
        logfile = "unittest_ECF_failed.log"
        server = scheduler.EcflowServer(ecf_host, ecf_port, logfile)

        def_file = "unittest_test_ecflow_failed.def"
        suite_name = "test_ecflow_failed"
        suite = scheduler.EcflowSuite(suite_name, def_file=def_file)
        fam = scheduler.EcflowSuiteFamily("My_family", suite)
        var = scheduler.EcflowSuiteVariable("ECF_PASS", "FREE")
        scheduler.EcflowSuiteTask("My_task", fam, variables=var)

        suite.save_as_defs()
        server.start_server()
        server.replace(suite_name, def_file)
        server.begin_suite(suite_name)

        ecf_name = "/test_ecflow_failed/My_family/My_task"
        ecf_pass = "FREE"
        ecf_tryno = "1"
        task = scheduler.EcflowTask(ecf_name, ecf_tryno, ecf_pass, ecf_rid=None)

        with self.assertRaises(Exception) as cm:
            with scheduler.EcflowClient(server, task) as ci:
                print("Running task ")
                raise Exception()
