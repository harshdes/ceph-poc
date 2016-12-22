import socket
import subprocess
import datetime
import logging
import tempfile
import config
import os
import paramiko as paramiko
from yaml import safe_load, dump

default_level = "INFO"
debug_logfile = None
debug_handler = None
error_logfile = None
error_handler = None
info_handler = None
log_formatter = None


# noinspection PyBroadException
def netcat(hostname, port):
    """
    http://bt3gl.github.io/black-hat-python-networking-the-socket-module.html
    :param hostname:
    :param port:
    :return:
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((hostname, port))
        s.shutdown(socket.SHUT_WR)
        return True
    except:
        return False
    finally:
        s.close()


def do_global_config(log_level=default_level, log_basedir=None):
    """May be run once only. Configures where logs are put and how they
    are formatted.

    :param log_level: default log level to use for new loggers
    :type log_level: str
    :param log_basedir: base directory in which to create log directory
    :type log_basedir: str

    :return: None
    """
    global default_level
    global debug_logfile
    global debug_handler
    global error_logfile
    global error_handler
    global info_handler
    global log_formatter
    if (debug_logfile and error_logfile and debug_handler and error_handler
        and log_formatter):
        # this is not the first run
        return
    # set up the directory name to create our log files in
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S%f")
    logdir_name = "cassandra_utils_" + timestamp
    numeric_level = getattr(logging, log_level.upper(), None)
    if isinstance(numeric_level, int):
        # reset default level to user-specified
        default_level = log_level
    # strings for log formatting
    log_format = ("%(asctime)s | %(levelname)s | %(name)s"
                  " | %(threadName)s: %(message)s")
    date_format = "%Y-%m-%d %H:%M:%S"
    # create a Formatter object using those strings (for use with non-root loggers)
    log_formatter = logging.Formatter(fmt=log_format, datefmt=date_format)
    logging.basicConfig(format=log_format, datefmt=date_format,
                        level=log_level)
    if log_basedir:
        logdir = os.path.join(log_basedir, logdir_name)
    else:
        logdir = os.path.join(tempfile.gettempdir(), logdir_name)
    os.mkdir(logdir)
    # store log location in log directory for future reference
    config.logdir = logdir
    # set up debug log file
    debug_logfile = os.path.join(logdir, "debug_log.txt")
    debug_handler = logging.FileHandler(debug_logfile, "w")
    debug_handler.setLevel(logging.DEBUG)
    debug_handler.setFormatter(log_formatter)

    # set up info handler (same log file as debug)
    info_handler = logging.FileHandler(debug_logfile, "w")
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(log_formatter)

    # set up error log file
    error_logfile = os.path.join(logdir, "error_log.txt")
    error_handler = logging.FileHandler(error_logfile, "w")
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(log_formatter)
    # add handlers to root logger
    logging.root.addHandler(debug_handler)
    logging.root.addHandler(error_handler)


class CmdHelper(object):
    """
    classdocs
    """

    def __init__(self):
        self.logger = Logger(name="cmd_helper")

    def run_cmd(self, command=None, silent=False):
        """
        :param silent:
        :param command: Command to run
        :return:
        """
        try:
            if not silent:
                self.logger.debug("Running command: {cmd}".format(cmd=command))
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
            if not silent:
                self.logger.debug("command: {cmd} output: {out}".format(cmd=command, out=output))
            return output.strip()
        except subprocess.CalledProcessError as err:
            if not silent:
                self.logger.error("Problem running cmd: {cmd} error: {error}".format(cmd=command, error=err.output))

        return None

    def run_remote_cmd(self, cmd=None, host=None, host_user=None, host_password=None):
        """

        :param cmd:
        :param host:
        :param host_user:
        :param host_password:
        :return:
        """
        with SSHConnection(host, host_user, host_password) as client:
            self.logger.info(client)
            stdin, stdout, stderr = client.exec_command(cmd)
            # get command results
            try:
                output = "".join(stdout.readlines()).strip()
                error_output = "".join(stderr.readlines()).strip()
            except UnicodeEncodeError:
                self.logger.info("Output is not in valid format")
                output = 'output is not in asci codec'
                error_output = 'no error'
            except UnicodeDecodeError:
                self.logger.info("Output is not in valid format")
                output = 'output is not in asci codec'
                error_output = 'no error'
            ret_code = stdout.channel.recv_exit_status()

        self.logger.debug("Return code: {ret_code}".format(retcode=ret_code))
        if output:
            self.logger.debug("On stdout:\n{output}\n".format(
                output=output))

        if error_output:
            self.logger.error("On stderr:\n{error}\n".format(
                error=error_output.encode('ascii', 'ignore')))


class Logger(logging.Logger):
    """A basic logger with handlers pre-configured for convenience."""

    def __init__(self, name=None, log_level=None, ):
        """Create logger object.

        :param name: logger name to pass to logging.Logger's __init__
        :type name: str
        :param log_level: log level to set for this logger's console
            output
        :type log_level: str
        """
        # first, create logger object normally
        super(Logger, self).__init__(name)
        if not log_level:
            log_level = default_level
        # don't propagate messages logged at this level to the root
        # logger
        self.propagate = False
        # do make sure we capture everything logged through this
        # logger, though
        self.setLevel(logging.DEBUG)
        # set up console logging
        numeric_level = getattr(logging, log_level.upper(), None)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_formatter)
        console_handler.setLevel(numeric_level)
        self.addHandler(console_handler)
        # attach debug and error handlers to take care of logging to
        # the proper files
        self.addHandler(debug_handler)
        self.addHandler(error_handler)
        self.addHandler(info_handler)


def read_yaml_file(file_path=None):
    try:
        file_handle = open(file_path, 'r')
        data = safe_load(file_handle)
        return data
    finally:
        if file_handle:
            file_handle.close()


def write_yaml_file(file_path=None, data_dict=None):
    """

    """
    try:
        file_handle = open(file_path, 'w')
        dump(data_dict, file_handle)
    finally:
        if file_handle:
            file_handle.close()


class SSHConnection(object):
    """Wrapper class to create and destroy paramiko SSH connection."""

    def __init__(self, address, username, password):
        """Set up the necessary information for this connection.

        :param address: IP or name used to connect to the system
        :type address: str
        :param username: username to use in authentication
        :type username: str
        :param password: password to use in authentication
        :type password: str
        """
        self.address = address
        self.username = username
        self.password = password

    def __enter__(self):
        """Create the SSH client and connect to the host. Used
        automatically through Python's "with" keyword.

        :return: paramiko.SSHClient object ready to use
        :rtype: :class:`paramiko.SSHClient`
        """
        self.client = paramiko.SSHClient()

        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(self.address, username=self.username,
                            password=self.password, allow_agent=False,
                            look_for_keys=False)
        return self.client

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close the SSH client's connection to the host. Used
        automatically through Python's "with" keyword.

        Parameters are standard:

        :param exc_type: exception type, if any, seen
        :type exc_type: type
        :param exc_val: exception seen
        :type exc_val: Exception
        :param exc_tb: traceback related to the exception
        :type exc_tb: traceback
        """
        self.client.close()

