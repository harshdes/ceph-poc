import subprocess
import datetime
import logging
import tempfile
import config
import os

default_level = "INFO"
debug_logfile = None
debug_handler = None
error_logfile = None
error_handler = None
log_formatter = None


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
    # create a Formatter object using those strings (for use with non-root
    # loggers)
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
    # set up error log file
    error_logfile = os.path.join(logdir, "error_log.txt")
    error_handler = logging.FileHandler(error_logfile, "w")
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(log_formatter)
    # add handlers to root logger
    logging.root.addHandler(debug_handler)
    logging.root.addHandler(error_handler)


class Cmd_helper(object):
    '''
    classdocs
    '''

    def __init__(self, logger=None):
        self.logger = logger

    def run_cmd(self, command=None):
        """
        :param command: Command to run
        :return:
        """
        try:
            self.logger.debug("Running command: {cmd}".format(cmd=command))
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
            return output
        except subprocess.CalledProcessError as err:
            self.logger.error("Problem running cmd: {cmd} error: {error}".format(cmd=command, error=err.output))

        return None


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
