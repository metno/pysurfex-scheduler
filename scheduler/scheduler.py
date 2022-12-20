"""Scheduler module."""
from abc import ABC, abstractmethod
import subprocess
import os
from datetime import datetime
import signal
import time
import platform
import traceback
import sys
import shutil
import json
import logging
try:
    import ecflow  # noqa reportMissingImports
except ModuleNotFoundError:
    ecflow = None


# Base Scheduler server class
class Server(ABC):
    """Base server/scheduler class."""

    def __init__(self):
        """Construct the server."""
        self.settings = None

    @abstractmethod
    def start_server(self):
        """Start the server.

        Raises:
            NotImplementedError: Must be implemented by the child server object.
        """
        raise NotImplementedError

    @abstractmethod
    def replace(self, suite_name, def_file):
        """Create or change the suite definition.

        Args:
            suite_name (str): Name of the suite.
            def_file (str): Name of the definition file.

        Raises:
            NotImplementedError: Must be implemented by the child server object.

        """
        raise NotImplementedError

    @abstractmethod
    def begin_suite(self, suite_name):
        """Begin the suite in a server specific way.

        Args:
            suite_name (str): Name of the suite

        Raises:
            NotImplementedError: Must be implemented by the child server object.
        """
        raise NotImplementedError

    def start_suite(self, suite_name, def_file, begin=True):
        """Start the suite.

        All the servers have these methods implemented and can start the server in a
        server specific way.

        Args:
            suite_name (str): Name of the suite
            def_file (str): Name of the definition file.
            begin (bool, optional): If the suite should begin. Defaults to True.
        """
        self.start_server()
        self.replace(suite_name, def_file)
        if begin:
            self.begin_suite(suite_name)


class EcflowServer(Server):
    """Ecflow server.

    Args:
        Server (Server): Is a child of the base server.
    """

    def __init__(self, ecf_host, ecf_port=3141, start_command=None, dry_run=False):
        """Construct the EcflowServer.

        Args:
            ecf_host(str): Ecflow server host.
            ecf_port (int): Ecflow server port.
            start_command: Ecflow start server command.
            dry_run(bool): Handle not running eflow server.

        Raises:
            Exception: If not ecflow is found.

        """
        if ecflow is None:
            if not dry_run:
                raise Exception("Ecflow was not found")
        Server.__init__(self)
        self.ecf_host = ecf_host
        self.ecf_port = ecf_port
        self.start_command = start_command
        if dry_run:
            self.ecf_client = None
        else:
            self.ecf_client = ecflow.Client(self.ecf_host, self.ecf_port)
        self.settings = {"ECF_HOST": self.ecf_host, "ECF_PORT": self.ecf_port}

    def start_server(self):
        """Start the server.

        Raises:
            RuntimeError: Server is not running or Could not restart server.
        """
        logging.debug("Start EcFlow server")
        try:
            logging.info("%s %s", self.ecf_host, self.ecf_port)
            if self.ecf_client is not None:
                self.ecf_client.ping()
            logging.info("EcFlow server is already running")
        except RuntimeError:
            logging.info("Re-Start EcFlow server")
            try:
                # Start server

                start_command = self.start_command
                if self.start_command is None:
                    start_command = f"ecflow_start.sh -p {str(self.ecf_port)}"

                logging.info(start_command)
                # TODO
                ret = os.system(start_command)  # noqa
                if ret != 0:
                    raise RuntimeError from RuntimeError
            except RuntimeError as error:
                raise RuntimeError("Could not restart server!") from error

    def begin_suite(self, suite_name):
        """Begin the suite.

        Args:
            suite_name (str): Nam eof the suite.
        """
        if self.ecf_client is not None:
            self.ecf_client.begin_suite(suite_name)

    def force_complete(self, task):
        """Force the task complete.

        Args:
            task (scheduler.EcflowTask): Task to force complete.
        """
        ecf_name = task.ecf_name
        if self.ecf_client is not None:
            self.ecf_client.force_state(ecf_name, ecflow.State.complete)

    def force_aborted(self, task):
        """Force the task aborted.

        Args:
            task (scheduler.EcflowTask): Task to force aborted.
        """
        ecf_name = task.ecf_name
        if self.ecf_client is not None:
            self.ecf_client.force_state(ecf_name, ecflow.State.aborted)

    def replace(self, suite_name, def_file):
        """Replace the suite name from def_file.

        Args:
            suite_name (str): Suite name.
            def_file (str): Definition file.

        Raises:
            Exception: _description_
        """
        logging.debug("%s %s", suite_name, def_file)
        if self.ecf_client is not None:
            try:
                self.ecf_client.replace("/" + suite_name, def_file)
            except RuntimeError:
                try:
                    self.ecf_client.delete("/" + suite_name)
                    self.ecf_client.replace("/" + suite_name, def_file)
                except RuntimeError:
                    raise Exception(
                        "Could not replace suite " + suite_name
                    ) from RuntimeError


class EcflowServerFromFile(EcflowServer):
    """Construct an ecflow server from a config file."""

    def __init__(self, ecflow_server_file):
        """Construct EcflowServer from a file.

        Args:
            ecflow_server_file (str): File with server definition

        Raises:
            FileNotFoundError: if server file was not found.
        """
        if os.path.exists(ecflow_server_file):
            with open(ecflow_server_file, mode="r", encoding="UTF-8") as file_handler:
                self.settings = json.load(file_handler)
        else:
            raise FileNotFoundError("Could not find " + ecflow_server_file)

        ecf_host = self.get_var("ECF_HOST")
        ecf_port_offset = int(self.get_var("ECF_PORT_OFFSET", default=1500))
        ecf_port = int(self.get_var("ECF_PORT", default=int(os.getuid())))
        ecf_port = ecf_port + ecf_port_offset

        EcflowServer.__init__(self, ecf_host, ecf_port)

    def get_var(self, var, default=None):
        """Get variable setting.

        Args:
            var (str): Key in settings.
            default (_type_, optional): _description_. Defaults to None.

        Raises:
            Exception: _description_

        Returns:
            _type_: _description_
        """
        if var in self.settings:
            return self.settings[var]

        if default is not None:
            return default
        else:
            raise Exception("Variable " + var + " not found!")

    def save_as_file(self, fname):
        """Save the server settings to a file.

        Args:
            fname (str): File name
        """
        with open(fname, mode="w", encoding="utf-8") as server_file:
            json.dump(self.settings, server_file)


class EcflowLogServer():
    """Ecflow log server."""

    def __init__(self, config):
        """Constuct the ecflow log server.

        Args:
            config (dict): Configuration
        """
        self.config = config
        self.ecf_loghost = config.get("ECF_LOGHOST")
        self.ecf_logport = config.get("ECF_LOGPORT")


class EcflowTask():
    """Ecflow scheduler task."""

    def __init__(self, ecf_name, ecf_tryno, ecf_pass, ecf_rid, ecf_timeout=20):
        """Construct a task running and communicating with ecflow server.

        Args:
            ecf_name (str): Full name of ecflow task.
            ecf_tryno (int): Ecflow task try number
            ecf_pass (str): Ecflow task password
            ecf_rid (int): Ecflow runtime ID
            ecf_timeout (int, optional): _description_. Defaults to 20.

        """
        self.ecf_name = ecf_name
        self.ecf_tryno = int(ecf_tryno)
        self.ecf_pass = ecf_pass
        if ecf_rid == "" or ecf_rid is None:
            ecf_rid = os.getpid()
        self.ecf_rid = int(ecf_rid)
        self.ecf_timeout = int(ecf_timeout)
        ecf_name_parts = self.ecf_name.split("/")
        self.ecf_task = ecf_name_parts[-1]
        ecf_families = None
        if len(ecf_name_parts) > 2:
            ecf_families = ecf_name_parts[1:-1]
        self.ecf_families = ecf_families
        self.family1 = None
        if self.ecf_families is not None:
            self.family1 = self.ecf_families[-1]


class EcflowClient(object):
    """An ecflow client.

    Encapsulate communication with the ecflow server. This will automatically call
    the child command init()/complete(), for job start/finish. It will also
    handle exceptions and signals, by calling the abort child command.
    *ONLY* one instance of this class, should be used. Otherwise zombies will be created.
    """

    def __init__(self, server, task, dry_run=False):
        """Construct the ecflow client.

        Args:
            server (EcflowServer): Ecflow server object.
            task (EcflowTask): Ecflow task object.
            dry_run(bool): Handle not running eflow server.

        """
        logging.debug("Creating Client")
        self.server = server
        if dry_run:
            self.client = None
        else:
            self.client = server.ecf_client
            # self.ci.set_host_port("%ECF_HOST%", "%ECF_PORT%") #noqa E800
            self.client.set_child_pid(task.ecf_rid)
            self.client.set_child_path(task.ecf_name)
            self.client.set_child_password(task.ecf_pass)
            self.client.set_child_try_no(task.ecf_tryno)
            logging.info(
                "   Only wait %s seconds, if the server cannot be contacted "
                "(note default is 24 hours) before failing",
                str(task.ecf_timeout),
            )
            self.client.set_child_timeout(task.ecf_timeout)
        self.task = task

        # Abort the task for the following signals
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGHUP, self.signal_handler)
        signal.signal(signal.SIGQUIT, self.signal_handler)
        signal.signal(signal.SIGILL, self.signal_handler)
        signal.signal(signal.SIGTRAP, self.signal_handler)
        signal.signal(signal.SIGIOT, self.signal_handler)
        signal.signal(signal.SIGBUS, self.signal_handler)
        signal.signal(signal.SIGFPE, self.signal_handler)
        signal.signal(signal.SIGUSR1, self.signal_handler)
        signal.signal(signal.SIGUSR2, self.signal_handler)
        signal.signal(signal.SIGPIPE, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        signal.signal(signal.SIGXCPU, self.signal_handler)
        if platform.system() != "Darwin":
            signal.signal(signal.SIGPWR, self.signal_handler)

    @staticmethod
    def at_time():
        """Generate time stamp.

        Returns:
            str: Time stamp.
        """
        return datetime.fromtimestamp(time.time()).strftime("%H:%M:%S")

    def signal_handler(self, signum, extra=None):
        """Signal handler.

        Args:
            signum (_type_): _description_
            extra (_type_, optional): _description_. Defaults to None.
        """
        logging.info("   Aborting: Signal handler called with signal %s", str(signum))

        self.__exit__(
            Exception, "Signal handler called with signal " + str(signum), extra
        )

    def __enter__(self):
        """Enter the object.

        Returns:
            _type_: _description_
        """
        logging.info("Calling init at: %s", self.at_time())
        if self.client is not None:
            self.client.child_init()
        return self.client

    def __exit__(self, ex_type, value, tback):
        """Exit method.

        Args:
            ex_type (_type_): _description_
            value (_type_): _description_
            tback (_type_): _description_

        Returns:
            _type_: _description_
        """
        logging.info("   Client:__exit__: ex_type: %s value: %s", str(ex_type), str(value))
        if ex_type is not None:
            logging.info("Calling abort %s", self.at_time())
            self.client.child_abort(
                f"Aborted with exception type {str(ex_type)}:{str(value)}"
            )
            if tback is not None:
                print(tback)
                traceback.print_tb(tback, limit=1, file=sys.stdout)
                print("*** print_exception:")
                # exc_type below is ignored on 3.5 and later
                print("*** print_exc:")
                traceback.print_exc(limit=2, file=sys.stdout)
                print("*** format_exc, first and last line:")
                formatted_lines = traceback.format_exc().splitlines()
                print(formatted_lines[0])
                print(formatted_lines[-1])
                print("*** format_exception:")
                print("*** extract_tb:")
                print(repr(traceback.extract_tb(tback)))
                print("*** format_tb:")
                print(repr(traceback.format_tb(tback)))
                print("*** tb_lineno:", tback.tb_lineno)
            return False
        print("Calling complete at: " + self.at_time())
        # self.server.update_log(self.task.ecf_name + " complete") #noqa E800
        if self.client is not None:
            self.client.child_complete()
        return False
