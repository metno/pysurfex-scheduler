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
import toml
sys.path.insert(0, "/usr/lib/python3/dist-packages/")
try:
    import ecflow
except ModuleNotFoundError:
    ecflow = None


# Base Scheduler server class
class Server(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def start_server(self):
        raise NotImplementedError

    @abstractmethod
    def replace(self, suite_name, def_file):
        raise NotImplementedError

    @abstractmethod
    def begin_suite(self, suite_name):
        raise NotImplementedError

    def start_suite(self, defs, begin=True):
        def_file = defs.suite.def_file
        suite_name = defs.suite.name
        self.start_server()
        self.replace(suite_name, def_file)
        if begin:
            self.begin_suite(suite_name)


class EcflowServer(Server):
    def __init__(self, ecf_host, ecf_port, logfile, ):
        if ecflow is None:
            raise Exception("Ecflow was not found")
        Server.__init__(self)
        self.ecf_host = ecf_host
        self.ecf_port = ecf_port
        self.logfile = logfile
        self.ecf_client = ecflow.Client(self.ecf_host, self.ecf_port)

    def start_server(self):
        print("Start EcFlow server")
        try:
            self.ecf_client.ping()
            print("EcFlow server is already running")
        except RuntimeError:
            print("Re-Start EcFlow server")
            try:
                # Start server
                # self.ecf_client.restart_server()
                cmd = shutil.which("ecflow_start")
                if cmd is None:
                    cmd = shutil.which("ecflow_start.sh")
                if cmd is None:
                    raise Exception("ecflow_start not found")
                cmd = cmd + " -p " + str(self.ecf_port)
                print(cmd)
                ret = subprocess.call(cmd.split())
                if ret != 0:
                    raise RuntimeError
            except RuntimeError:
                raise Exception("Could not restart server!")

    def begin_suite(self, suite_name):
        self.ecf_client.begin_suite(suite_name)

    def force_complete(self, task):
        ecf_name = task.ecf_name
        self.ecf_client.force_state(ecf_name, ecflow.State.complete)

    def force_aborted(self, task):
        ecf_name = task.ecf_name
        self.ecf_client.force_state(ecf_name, ecflow.State.aborted)

    def update_submission_id(self, task):
        self.update_log(task.ecf_name)
        self.update_log(task.submission_id)
        print(task.ecf_name, "add", "variable", "SUBMISSION_ID", task.submission_id)
        self.ecf_client.alter(task.ecf_name, "add", "variable", "SUBMISSION_ID", task.submission_id)

    def replace(self, suite_name, def_file):
        print(suite_name, def_file)
        try:
            self.ecf_client.replace("/" + suite_name, def_file)
        except RuntimeError:
            try:
                self.ecf_client.delete("/" + suite_name)
                self.ecf_client.replace("/" + suite_name, def_file)
            except RuntimeError:
                raise Exception("Could not replace suite " + suite_name)

    def update_log(self, text):
        print(self.logfile)
        utcnow = datetime.utcnow().strftime("[%H:%M:%S %d.%m.%Y]")
        fh = open(self.logfile, "a")
        fh.write(utcnow + " " + str(text) + "\n")
        fh.flush()
        fh.close()


class EcflowServerFromFile(EcflowServer):
    def __init__(self, ecflow_server_file, logfile):
        if os.path.exists(ecflow_server_file):
            self.settings = toml.load(open(ecflow_server_file, "r"))
        else:
            raise FileNotFoundError("Could not find " + ecflow_server_file)

        ecf_host = self.get_var("ECF_HOST")
        ecf_port_offset = int(self.get_var("ECF_PORT_OFFSET", default=1500))
        ecf_port = int(self.get_var("ECF_PORT", default=int(os.getuid())))
        ecf_port = ecf_port + ecf_port_offset

        # logfile = self.get_var("SERVER_LOG")
        EcflowServer.__init__(self, ecf_host, ecf_port, logfile)

    def get_var(self, var, default=None):
        if var in self.settings:
            return self.settings[var]
        else:
            if default is not None:
                return default
            else:
                raise Exception("Variable " + var + " not found!")

    def save_as_file(self, wdir):
        fname = self.get_file_name(wdir)
        toml.dump(self.settings, open(fname,"w"))

    @staticmethod
    def get_file_name(wdir, full_path=False):
        f = "Env_server"
        if full_path:
            f = wdir + "/" + f
        return f


class EcflowLogServer(object):
    def __init__(self, ecf_loghost, ecf_logport):
        self.ecf_loghost = ecf_loghost
        self.ecf_logport = ecf_logport


class EcflowTask(object):
    def __init__(self, ecf_name, ecf_tryno, ecf_pass, ecf_rid, submission_id=None, ecf_timeout=20):
        self.ecf_name = ecf_name
        self.ecf_tryno = int(ecf_tryno)
        self.ecf_pass = ecf_pass
        if ecf_rid == "" or ecf_rid is None:
            ecf_rid = os.getpid()
        self.ecf_rid = int(ecf_rid)
        self.ecf_timeout = ecf_timeout
        ecf_name_parts = self.ecf_name.split("/")
        self.ecf_task = ecf_name_parts[-1]
        ecf_families = None
        if len(ecf_name_parts) > 2:
            ecf_families = ecf_name_parts[1:-1]
        self.ecf_families = ecf_families
        self.family1 = None
        if self.ecf_families is not None:
            self.family1 = self.ecf_families[-1]

        if submission_id == "":
            submission_id = None
        self.submission_id = submission_id

    def create_submission_log(self, joboutdir):
        return joboutdir + "/" + self.ecf_name + ".job" + str(self.ecf_tryno) + ".sub"

    def create_kill_log(self, joboutdir):
        return joboutdir + "/" + self.ecf_name + ".job" + str(self.ecf_tryno) + ".kill"

    def create_status_log(self, joboutdir):
        return joboutdir + "/" + self.ecf_name + ".job" + str(self.ecf_tryno) + ".stat"

    def create_ecf_job(self, joboutdir):
        return joboutdir + "/" + self.ecf_name + ".job" + str(self.ecf_tryno)

    def create_ecf_jobout(self, joboutdir):
        return joboutdir + "/" + self.ecf_name + "." + str(self.ecf_tryno)


class EcflowClient(object):
    """Encapsulate communication with the ecflow server. This will automatically call
       the child command init()/complete(), for job start/finish. It will also
       handle exceptions and signals, by calling the abort child command.
       *ONLY* one instance of this class, should be used. Otherwise zombies will be created.
    """

    def __init__(self, server, task):
        print("Creating Client")
        self.server = server
        self.ci = server.ecf_client
        # self.ci.set_host_port("%ECF_HOST%", "%ECF_PORT%")
        self.ci.set_child_pid(task.ecf_rid)
        self.ci.set_child_path(task.ecf_name)
        self.ci.set_child_password(task.ecf_pass)
        self.ci.set_child_try_no(task.ecf_tryno)
        print("   Only wait " + str(task.ecf_timeout) +
              " seconds, if the server cannot be contacted (note default is 24 hours) before failing")
        self.ci.set_child_timeout(task.ecf_timeout)
        # self.ci.set_zombie_child_timeout(10)
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
        return datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')

    def signal_handler(self, signum, extra=None):
        print('   Aborting: Signal handler called with signal ', signum)
        # self.ci.child_abort("Signal handler called with signal " + str(signum))
        self.__exit__(Exception, "Signal handler called with signal " + str(signum), None)

    def __enter__(self):
        print('Calling init at: ' + self.at_time())
        # self.server.update_log(self.task.ecf_name + " init")
        self.ci.child_init()
        return self.ci

    def __exit__(self, ex_type, value, tb):
        print("   Client:__exit__: ex_type:" + str(ex_type) + " value:" + str(value))
        if ex_type is not None:
            print('Calling abort ' + self.at_time())
            self.ci.child_abort("Aborted with exception type " + str(ex_type) + ":" + str(value))
            if tb is not None:
                print(tb)
                traceback.print_tb(tb, limit=1, file=sys.stdout)
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
                print(repr(traceback.extract_tb(tb)))
                print("*** format_tb:")
                print(repr(traceback.format_tb(tb)))
                print("*** tb_lineno:", tb.tb_lineno)
                self.server.update_log(self.task.ecf_name + " abort")
            return False
        print('Calling complete at: ' + self.at_time())
        # self.server.update_log(self.task.ecf_name + " complete")
        self.ci.child_complete()
        return False

