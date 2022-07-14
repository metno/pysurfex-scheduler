"""Scheduler module."""
import sys
from argparse import ArgumentParser
import json
import os
import scheduler


def parse_submit_cmd(argv):
    """Parse the command line input arguments."""
    parser = ArgumentParser("ECF_submit task to ecflow")

    parser.add_argument('-sub', dest="env_submit", type=str, help="File with submission settings",
                        required=False)
    parser.add_argument('-dir', dest="joboutdir", type=str, help="Ecflow JOBOUTDIR", required=False)
    parser.add_argument('-server', dest="env_server", type=str,
                        help="File or with Ecflow server settings",
                        required=False)
    parser.add_argument('--log', dest="logfile", type=str, help="Server logfile", required=True)
    parser.add_argument('-ecf_name', type=str, help="Name of ECF Task")
    parser.add_argument('-ecf_tryno', type=str, help="ECF try number")
    parser.add_argument('-ecf_pass', type=str, help="Name of ECF password")

    parser.add_argument('-stream', type=str, nargs="?", help="Stream", required=False, default=None)
    parser.add_argument('-ecf_rid', nargs='?', type=str, default=None, required=False,
                        help="ECF remote id")
    parser.add_argument('-ensmbr', dest="ensmbr", nargs="?", type=int, help="Ensemble member",
                        required=False,
                        default=None)
    parser.add_argument('--db', dest="dbfile", type=str, nargs="?", help="Database",
                        required=False, default=None)
    parser.add_argument('--version', action='version', version=scheduler.__version__)

    if len(argv) == 0:
        parser.print_help()
        sys.exit()

    args = parser.parse_args(argv)
    kwargs = {}
    for arg in vars(args):
        kwargs.update({arg: getattr(args, arg)})
    return kwargs


def submit_cmd(**kwargs):
    """Submit command."""
    ecf_name = kwargs["ecf_name"]
    ensmbr = kwargs["ensmbr"]
    ecf_tryno = kwargs["ecf_tryno"]
    ecf_pass = kwargs["ecf_pass"]
    ecf_rid = kwargs["ecf_rid"]
    joboutdir = kwargs["joboutdir"]
    if isinstance(joboutdir, str):
        joboutdir = {"0": joboutdir}
    env_submit = kwargs["env_submit"]
    if isinstance(env_submit, str):
        with open(env_submit, mode="r", encoding="utf-8") as file_handler:
            env_submit = json.load(file_handler)
    env_server = kwargs["env_server"]
    logfile = kwargs["logfile"]
    if isinstance(env_server, str):
        env_server = scheduler.EcflowServerFromFile(env_server, logfile=logfile)
    else:
        env_server = scheduler.EcflowServer(env_server["ECF_HOST"], env_server["ECF_PORT"],
                                            logfile=logfile)

    env_file = kwargs.get("env_file")
    submission_id = None
    stream = kwargs.get("stream")
    dbfile = kwargs.get("dbfile")
    coldstart = False
    if "coldstart" in kwargs:
        coldstart = kwargs["coldstart"]

    if ecf_rid is not None:
        if ecf_rid == "":
            ecf_rid = os.getpid()
    else:
        ecf_rid = os.getpid()

    dry_run = kwargs.get("dry_run")
    if dry_run is None:
        dry_run = False

    try:
        task = scheduler.EcflowTask(ecf_name, ecf_tryno, ecf_pass, ecf_rid, submission_id)
        sub = scheduler.EcflowSubmitTask(task, env_submit, env_server, joboutdir,
                                         env_file=env_file, ensmbr=ensmbr,
                                         dbfile=dbfile, stream=stream, coldstart=coldstart)
        if not dry_run:
            sub.submit()
    except Exception as ex:
        raise ex


def parse_kill_cmd(argv):
    """Parse the command line input arguments."""
    parser = ArgumentParser("Kill EcFlow task and handle abort")
    parser.add_argument("-sub", dest='env_submit', type=str, help="File with submission settings",
                        required=True)
    parser.add_argument('-dir', dest="joboutdir", type=str, help="Ecflow JOBOUTDIR", required=True)
    parser.add_argument("-server", dest='env_server', type=str,
                        help="File with Ecflow server settings", required=True)
    parser.add_argument('--log', dest="logfile", type=str, help="Server logfile", required=True)
    parser.add_argument("-ecf_name", dest='ecf_name', type=str, help="ECF_NAME", required=True)
    parser.add_argument("-ecf_tryno", dest='ecf_tryno', type=str, help="ECF_TRYNO", required=True)
    parser.add_argument("-ecf_pass", dest='ecf_pass', type=str, help="ECF_PASS", required=True)
    parser.add_argument('-ecf_rid', dest='ecf_rid', type=str, help="ECF_RID", required=False,
                        nargs="?", default=None)
    parser.add_argument('-submission_id', type=str, help="SUBMISSION_ID")
    parser.add_argument('--version', action='version', version=scheduler.__version__)

    if len(argv) == 0:
        parser.print_help()
        sys.exit()

    args = parser.parse_args(argv)
    kwargs = {}
    for arg in vars(args):
        kwargs.update({arg: getattr(args, arg)})
    return kwargs


def kill_cmd(**kwargs):
    """Kill cmmand."""
    ecf_name = kwargs["ecf_name"]
    ecf_tryno = kwargs["ecf_tryno"]
    ecf_pass = kwargs["ecf_pass"]
    ecf_rid = kwargs["ecf_rid"]
    submission_id = ""
    if "submission_id" in kwargs:
        submission_id = kwargs["submission_id"]
    if submission_id == "":
        submission_id = None
    env_submit = kwargs["env_submit"]
    if isinstance(env_submit, str):
        with open(env_submit, mode="r", encoding="utf-8") as file_handler:
            env_submit = json.load(file_handler)
    jobout_dir = kwargs["joboutdir"]
    if isinstance(jobout_dir, str):
        jobout_dir = {"0": jobout_dir}

    server = kwargs["env_server"]
    # If a server environment file, create a server
    if isinstance(server, str):
        logfile = kwargs["logfile"]
        server = scheduler.EcflowServerFromFile(server, logfile)

    dry_run = False
    if "dry_run" in kwargs:
        dry_run = kwargs["dry_run"]

    task = scheduler.EcflowTask(ecf_name, ecf_tryno, ecf_pass, ecf_rid, submission_id)
    task_settings = scheduler.TaskSettings(task, env_submit, jobout_dir)
    # print(task.submission_id)
    sub = scheduler.get_submission_object(task, task_settings, server)
    # print(sub)
    if not dry_run:
        sub.kill()
        server.force_aborted(task)


def parse_status_cmd(argv):
    """Parse the command line input arguments."""
    parser = ArgumentParser("Status of EcFlow task")

    parser.add_argument("-sub", dest='env_submit', type=str, help="File with submission settings",
                        required=True)
    parser.add_argument('-dir', dest="joboutdir", type=str, help="Ecflow JOBOUTDIR", required=True)
    parser.add_argument("-server", dest='env_server', type=str,
                        help="File with Ecflow server settings", required=True)
    parser.add_argument('--log', dest="logfile", type=str, help="Server logfile", required=True)
    parser.add_argument('-ecf_name', type=str, help="ECF_NAME", required=True)
    parser.add_argument('-ecf_tryno', type=str, help="ECF_TRYNO", required=True)
    parser.add_argument('-ecf_pass', type=str, help="ECF_PASS", required=True)
    parser.add_argument('-ecf_rid', type=str, help="ECF_RID", required=False, nargs="?",
                        default=None)
    parser.add_argument('-submission_id', type=str, help="SUBMISSION_ID")
    parser.add_argument('--version', action='version', version=scheduler.__version__)

    if len(argv) == 0:
        parser.print_help()
        sys.exit()

    args = parser.parse_args(argv)
    kwargs = {}
    for arg in vars(args):
        kwargs.update({arg: getattr(args, arg)})
    return kwargs


def status_cmd(**kwargs):
    """Status command."""
    ecf_name = kwargs["ecf_name"]
    ecf_tryno = kwargs["ecf_tryno"]
    ecf_pass = kwargs["ecf_pass"]
    ecf_rid = kwargs["ecf_rid"]
    submission_id = kwargs["submission_id"]
    env_submit = kwargs["env_submit"]
    if isinstance(env_submit, str):
        with open(env_submit, mode="r", encoding="utf-8") as file_handler:
            env_submit = json.load(file_handler)
    jobout_dir = kwargs["joboutdir"]
    if isinstance(jobout_dir, str):
        jobout_dir = {"0": jobout_dir}

    dry_run = False
    if "dry_run" in kwargs:
        dry_run = kwargs["dry_run"]

    server = kwargs["env_server"]
    # If a server environment file, create a server
    if isinstance(server, str):
        logfile = kwargs["logfile"]
        server = scheduler.EcflowServerFromFile(server, logfile)

    task = scheduler.EcflowTask(ecf_name, ecf_tryno, ecf_pass, ecf_rid, submission_id)
    task_settings = scheduler.TaskSettings(task, env_submit, jobout_dir)

    sub = scheduler.get_submission_object(task, task_settings, server)
    if not dry_run:
        sub.status()
