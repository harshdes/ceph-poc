import logging
import os
import socket
import subprocess

import paramiko as paramiko
from yaml import safe_load, dump


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


def setup_logging(
        default_path='apis-utils/config/logging.yaml',
        default_level=logging.INFO
):
    """Setup logging configuration

    """
    path = default_path
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


class CmdHelper(object):
    """
    classdocs
    """

    def __init__(self):
        self.logger = logging.getLogger("apis")

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

        self.logger.debug("Return code: {ret_code}".format(ret_code=ret_code))
        if output:
            self.logger.debug("On stdout:\n{output}\n".format(
                output=output))

        if error_output:
            self.logger.error("On stderr:\n{error}\n".format(
                error=error_output.encode('ascii', 'ignore')))


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
