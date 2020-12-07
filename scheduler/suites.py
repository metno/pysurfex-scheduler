import sys
import os
sys.path.insert(0, "/usr/lib/python3/dist-packages/")
try:
    import ecflow
except ImportError:
    ecflow = None


class SuiteDefinition(object):
    def __init__(self, suite_name, def_file, joboutdir, ecf_files, env_submit, server_config, server_log,
                 ecf_home=None, ecf_include=None, ecf_out=None, ecf_jobout=None,
                 ecf_job_cmd=None, ecf_status_cmd=None, ecf_kill_cmd=None, pythonpath="", path=""):

        if ecflow is None:
            raise Exception("Ecflow not loaded properly")

        name = suite_name
        self.joboutdir = joboutdir
        if ecf_include is None:
            ecf_include = ecf_files
        self.ecf_include = ecf_include
        self.ecf_files = ecf_files
        if ecf_home is None:
            ecf_home = joboutdir
        self.ecf_home = ecf_home
        if ecf_out is None:
            ecf_out = joboutdir
        self.ecf_out = ecf_out
        if ecf_jobout is None:
            ecf_jobout = joboutdir + "/%ECF_NAME%.%ECF_TRYNO%"
        self.ecf_jobout = ecf_jobout

        self.env_submit = env_submit
        self.server_config = server_config
        self.server_log = server_log

        if pythonpath != "":
            pythonpath = pythonpath + "; "
        if path != "":
            path = path + "/"
        if ecf_job_cmd is None:
            ecf_job_cmd =  pythonpath + path + "ECF_submit " \
                                   "-sub %ENV_SUBMIT% " \
                                   "-dir %ECF_OUT% " \
                                   "-server %SERVER_CONFIG% " \
                                   "--log %LOGFILE% " \
                                   "-ecf_name %ECF_NAME% " \
                                   "-ecf_tryno %ECF_TRYNO% " \
                                   "-ecf_pass %ECF_PASS% " \
                                   "-ecf_rid %ECF_RID% "
        self.ecf_job_cmd = ecf_job_cmd
        if ecf_status_cmd is None:
            ecf_status_cmd = pythonpath + path + "ECF_status " \
                                   "-dir %ECF_OUT% " \
                                   "-ecf_name %ECF_NAME% " \
                                   "-ecf_tryno %ECF_TRYNO% " \
                                   "-ecf_pass %ECF_PASS% " \
                                   "-ecf_rid %ECF_RID% " \
                                   "-submission_id %SUBMISSION_ID%"

        self.ecf_status_cmd = ecf_status_cmd
        if ecf_kill_cmd is None:
            ecf_kill_cmd = pythonpath + path + "ECF_kill " \
                                   "-sub %ENV_SUBMIT% " \
                                   "-dir %ECF_OUT% " \
                                   "-server %SERVER_CONFIG% " \
                                   "--log %LOGFILE% " \
                                   "-ecf_name %ECF_NAME% " \
                                   "-ecf_tryno %ECF_TRYNO% " \
                                   "-ecf_pass %ECF_PASS% " \
                                   "-ecf_rid %ECF_RID% " \
                                   "-submission_id %SUBMISSION_ID%"
        self.ecf_kill_cmd = ecf_kill_cmd

        variables = [EcflowSuiteVariable("ECF_EXTN", ".py"),
                     EcflowSuiteVariable("STREAM", ""),
                     EcflowSuiteVariable("ENSMBR", ""),
                     EcflowSuiteVariable("ECF_FILES", self.ecf_files),
                     EcflowSuiteVariable("ECF_INCLUDE", self.ecf_include),
                     EcflowSuiteVariable("ECF_TRIES", 1),
                     EcflowSuiteVariable("SUBMISSION_ID", ""),
                     EcflowSuiteVariable("ECF_HOME", self.ecf_home),
                     EcflowSuiteVariable("ECF_KILL_CMD", self.ecf_kill_cmd),
                     EcflowSuiteVariable("ECF_JOB_CMD", self.ecf_job_cmd),
                     EcflowSuiteVariable("ECF_STATUS_CMD", self.ecf_status_cmd),
                     EcflowSuiteVariable("ECF_OUT", self.ecf_out),
                     EcflowSuiteVariable("ECF_JOBOUT", self.ecf_jobout),
                     EcflowSuiteVariable("ENV_SUBMIT", self.env_submit),
                     EcflowSuiteVariable("SERVER_CONFIG", self.server_config),
                     EcflowSuiteVariable("LOGFILE", self.server_log)

        ]

        self.suite = EcflowSuite(name, def_file=def_file, variables=variables)

    def save_as_defs(self):
        self.suite.save_as_defs()


class EcflowNode(object):

    """
    A Node class is the abstract base class for Suite, Family and Task

    Every Node instance has a name, and a path relative to a suite
    """

    def __init__(self, name, node_type, parent, **kwargs):
        self.name = name
        self.node_type = node_type

        if self.node_type == "family":
            self.ecf_node = parent.ecf_node.add_family(self.name)
        elif self.node_type == "task":
            self.ecf_node = parent.ecf_node.add_task(self.name)
        elif self.node_type == "suite":
            self.ecf_node = parent.add_suite(self.name)
        else:
            raise NotImplementedError

        self.path = self.ecf_node.get_abs_node_path()
        triggers = None
        if "triggers" in kwargs:
            triggers = kwargs["triggers"]

        variables = None
        if "variables" in kwargs:
            variables = kwargs["variables"]
        self.variables = variables

        if self.variables is not None:
            if not isinstance(self.variables, list):
                self.variables = [self.variables]
            for v in self.variables:
                self.ecf_node.add_variable(v.name, v.value)

        if triggers is not None:
            if isinstance(triggers, EcflowSuiteTriggers):
                if triggers.trigger_string is not None:
                    self.ecf_node.add_trigger(triggers.trigger_string)
                else:
                    print("WARNING: Empty trigger")
            else:
                raise Exception("Triggers must be a Triggers object")
        self.triggers = triggers

        if "def_status" in kwargs:
            def_status = kwargs["def_status"]
            if isinstance(def_status, str):
                self.ecf_node.add_defstatus(ecflow.Defstatus(def_status))
            elif isinstance(def_status, ecflow.Defstatus):
                self.ecf_node.add_defstatus(def_status)
            else:
                raise Exception("Unknown defstatus")

    def add_part_trigger(self, triggers, mode=True):
        if isinstance(triggers, EcflowSuiteTriggers):
            if triggers.trigger_string is not None:
                self.ecf_node.add_part_trigger(triggers.trigger_string, mode)
            else:
                print("WARNING: Empty trigger")
        else:
            raise Exception("Triggers must be a Triggers object")


class EcflowNodeContainer(EcflowNode):
    def __init__(self, name, node_type, parent, **kwargs):
        EcflowNode.__init__(self, name, node_type, parent, **kwargs)


class EcflowSuite(EcflowNodeContainer):
    def __init__(self, name, **kwargs):
        self.defs = ecflow.Defs({})

        def_file = None
        if "def_file" in kwargs:
            def_file = kwargs["def_file"]
        self.def_file = def_file
        if def_file is None:
            self.def_file = name + ".def"
        EcflowNodeContainer.__init__(self, name, "suite", self.defs, **kwargs)

    def save_as_defs(self):
        self.defs.save_as_defs(self.def_file)
        print("def file saved to " + self.def_file)


class EcflowSuiteTriggers(object):
    def __init__(self, triggers, **kwargs):
        mode = "AND"
        if "mode" in kwargs:
            mode = kwargs["mode"]
        trigger_string = self.create_string(triggers, mode)
        self.trigger_string = trigger_string

    @staticmethod
    def create_string(trigs, mode):
        triggers = trigs
        if not isinstance(triggers, list):
            triggers = [triggers]

        if len(triggers) == 0:
            raise Exception

        trigger = "("
        first = True
        for t in triggers:
            if t is not None:
                a = ""
                if not first:
                    a = " " + mode + " "
                if isinstance(t, EcflowSuiteTriggers):
                    trigger = trigger + a + t.trigger_string
                else:
                    if isinstance(t, EcflowSuiteTrigger):
                        trigger = trigger + a + t.node.path + " == " + t.mode
                    else:
                        raise Exception("Trigger must be a Trigger object")
                first = False
        trigger = trigger + ")"
        # If no triggers were found/set
        if first:
            trigger = None
        return trigger

    def add_triggers(self, triggers, mode="AND"):
        a = " " + mode + " "
        trigger_string = self.create_string(triggers, mode)
        if trigger_string is not None:
            self.trigger_string = self.trigger_string + a + trigger_string


class EcflowSuiteTrigger(object):
    def __init__(self, node, mode="complete"):
        self.node = node
        self.mode = mode
        # self.path = self.node.ecf_node.get_abs_path()


class EcflowSuiteVariable(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value


class EcflowSuiteFamily(EcflowNodeContainer):
    def __init__(self, name, parent, **kwargs):
        EcflowNodeContainer.__init__(self, name, "family", parent, **kwargs)


class EcflowSuiteTask(EcflowNode):
    def __init__(self, name, parent, **kwargs):
        EcflowNode.__init__(self, name, "task", parent, **kwargs)

        ecf_files = None
        if "ecf_files" in kwargs:
            ecf_files = kwargs["ecf_files"]

        if ecf_files is not None:

            if name == "default":
                raise Exception("Job should not be called default")
            else:
                default_job = ecf_files + "/default.py"
                task_job = ecf_files + "/" + name + ".py"
                if not os.path.exists(task_job) and not os.path.islink(task_job):
                    print(default_job + " - > " + task_job)
                    os.symlink(default_job, task_job)
