"""Ecflow suites."""
import os
import logging
try:
    import ecflow
except ImportError:
    ecflow = None


class SuiteDefinition(object):
    """The definition of the suite.

    Args:
        object (_type_): _description_
    """

    def __init__(self, suite_name, joboutdir, ecf_files, env_submit,
                 ecf_home=None, ecf_include=None, ecf_out=None, ecf_jobout=None,
                 ecf_job_cmd=None, ecf_status_cmd=None, ecf_kill_cmd=None, pythonpath="", path=""):
        """Construct the definition.

        Args:
            suite_name (_type_): _description_
            joboutdir (_type_): _description_
            ecf_files (_type_): _description_
            env_submit (_type_): _description_
            ecf_home (_type_, optional): _description_. Defaults to None.
            ecf_include (_type_, optional): _description_. Defaults to None.
            ecf_out (_type_, optional): _description_. Defaults to None.
            ecf_jobout (_type_, optional): _description_. Defaults to None.
            ecf_job_cmd (_type_, optional): _description_. Defaults to None.
            ecf_status_cmd (_type_, optional): _description_. Defaults to None.
            ecf_kill_cmd (_type_, optional): _description_. Defaults to None.
            pythonpath (str, optional): _description_. Defaults to "".
            path (str, optional): _description_. Defaults to "".

        Raises:
            Exception: _description_

        """
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
        # self.server_config = server_config
        # self.server_log = server_log

        if pythonpath != "":
            pythonpath = pythonpath + "; "
        if path != "":
            path = path + "/"
        if ecf_job_cmd is None:
            ecf_job_cmd = pythonpath + path + "ECF_submit " \
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

        variables = [
            EcflowSuiteVariable("ECF_EXTN", ".py"),
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
            # EcflowSuiteVariable("SERVER_CONFIG", self.server_config),
            # EcflowSuiteVariable("LOGFILE", self.server_log)
        ]

        self.suite = EcflowSuite(name, variables=variables)

    def save_as_defs(self, def_file):
        """Save definition file.

        Args:
            def_file (str): Name of definition file
        """
        self.suite.save_as_defs(def_file)


class EcflowNode():
    """A Node class is the abstract base class for Suite, Family and Task.

    Every Node instance has a name, and a path relative to a suite
    """

    def __init__(self, name, node_type, parent, **kwargs):
        """Construct the EcflowNode.

        Args:
            name (_type_): _description_
            node_type (_type_): _description_
            parent (_type_): _description_

        Raises:
            NotImplementedError: _description_
            Exception: _description_
            Exception: _description_

        """
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

        if "variables" in kwargs:
            variables = kwargs["variables"]
            if not isinstance(variables, list):
                variables = [variables]
            if variables is None:
                variables = []
        else:
            variables = []

        for var in variables:
            self.ecf_node.add_variable(var.name, var.value)

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
        """Add a part trigger.

        Args:
            triggers (_type_): _description_
            mode (bool, optional): _description_. Defaults to True.

        Raises:
            Exception: _description_

        """
        if isinstance(triggers, EcflowSuiteTriggers):
            if triggers.trigger_string is not None:
                self.ecf_node.add_part_trigger(triggers.trigger_string, mode)
            else:
                print("WARNING: Empty trigger")
        else:
            raise Exception("Triggers must be a Triggers object")


class EcflowNodeContainer(EcflowNode):
    """Ecflow node container.

    Args:
        EcflowNode (EcflowNode): Parent class.
    """

    def __init__(self, name, node_type, parent, **kwargs):
        """Construct EcflowNodeContainer.

        Args:
            name (str): Name of the node container.
            node_type (str): What kind of node.
            parent (EcflowNode): Parent to this node.

        """
        EcflowNode.__init__(self, name, node_type, parent, **kwargs)


class EcflowSuite(EcflowNodeContainer):
    """EcflowSuite.

    Args:
        EcflowNodeContainer (EcflowNodeContainer): A child of the EcflowNodeContainer class.
    """

    def __init__(self, name, **kwargs):
        """Construct the Ecflow suite.

        Args:
            name (_type_): _description_

        """
        self.defs = ecflow.Defs({})

        EcflowNodeContainer.__init__(self, name, "suite", self.defs, **kwargs)

    def save_as_defs(self, def_file):
        """Save defintion file.

        Args:
            def_file (str): Name of the definition file.
        """
        self.defs.save_as_defs(def_file)
        logging.info("def file saved to %s", def_file)


class EcflowSuiteTriggers():
    """Triggers to an ecflow suite."""

    def __init__(self, triggers, **kwargs):
        """Construct EcflowSuiteTriggers.

        Args:
            triggers (list): List of EcflowSuiteTrigger objects.

        """
        mode = kwargs.get("mode")
        if mode is None:
            mode = "AND"

        trigger_string = self.create_string(triggers, mode)
        self.trigger_string = trigger_string

    @staticmethod
    def create_string(triggers, mode):
        """Create the trigger string.

        Args:
            triggers (list): List of trigger objects
            mode     (str): Concatenation type.

        Raises:
            Exception: _description_
            Exception: _description_

        Returns:
            str: The trigger string based on trigger objects.

        """
        if not isinstance(triggers, list):
            triggers = [triggers]

        if len(triggers) == 0:
            raise Exception

        trigger_string = "("
        first = True
        for trigger in triggers:
            if trigger is not None:
                cat = ""
                if not first:
                    cat = " " + mode + " "
                if isinstance(trigger, EcflowSuiteTriggers):
                    trigger_string = trigger_string + cat + trigger.trigger_string
                else:
                    if isinstance(trigger, EcflowSuiteTrigger):
                        trigger_string = trigger_string + cat + trigger.node.path + " == " +\
                                                                                    trigger.mode
                    else:
                        raise Exception("Trigger must be a Trigger object")
                first = False
        trigger_string = trigger_string + ")"
        # If no triggers were found/set
        if first:
            trigger_string = None
        return trigger_string

    def add_triggers(self, triggers, mode="AND"):
        """Add triggers.

        Args:
            triggers (EcflowSuiteTriggers): The triggers
            mode (str, optional): Cat mode. Defaults to "AND".

        """
        cat_string = " " + mode + " "
        trigger_string = self.create_string(triggers, mode)
        if trigger_string is not None:
            self.trigger_string = self.trigger_string + cat_string + trigger_string


class EcflowSuiteTrigger():
    """EcFlow Trigger in a suite."""

    def __init__(self, node, mode="complete"):
        """Create a EcFlow trigger object.

        Args:
            node (scheduler.EcflowNode): The node to trigger on
            mode (str):

        """
        self.node = node
        self.mode = mode


class EcflowSuiteVariable():
    """A variable in an ecflow suite."""

    def __init__(self, name, value):
        """Constuct the EcflowSuiteVariable.

        Args:
            name (str): Name
            value (str): Value

        """
        self.name = name
        self.value = value


class EcflowSuiteFamily(EcflowNodeContainer):
    """A family in ecflow.

    Args:
        EcflowNodeContainer (_type_): _description_
    """

    def __init__(self, name, parent, **kwargs):
        """Construct the family.

        Args:
            name (str): Name of the family.
            parent (EcflowNodeContainer): Parent node.

        """
        EcflowNodeContainer.__init__(self, name, "family", parent, **kwargs)


class EcflowSuiteTask(EcflowNode):
    """A task in an ecflow suite/family.

    Args:
        EcflowNode (EcflowNodeContainer): The node container.
    """

    def __init__(self, name, parent, **kwargs):
        """Constuct the EcflowSuiteTask.

        Args:
            name (str): Name of task
            parent (EcflowNode): Parent node.

        Raises:
            Exception: _description_
        """
        EcflowNode.__init__(self, name, "task", parent, **kwargs)

        ecf_files = kwargs.get("ecf_files")
        if ecf_files is not None:

            if name == "default":
                raise Exception("Job should not be called default")
            else:
                default_job = ecf_files + "/default.py"
                task_job = ecf_files + "/" + name + ".py"
                if not os.path.exists(task_job) and not os.path.islink(task_job):
                    print(default_job + " - > " + task_job)
                    os.symlink(default_job, task_job)
