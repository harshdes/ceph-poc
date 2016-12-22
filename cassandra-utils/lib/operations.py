'''
Created on Dec 20, 2016

@author: 25200
'''
from lib import cassandra_client
from lib.cassandra_client import cassandra_client
from lib.common_utils import Cmd_helper, Logger
from lib.constants import CassandraConstants
import time


def get_info():
    pass


def is_cassandra_running(cmd_helper=None, timeout=30, retry_interval=2):
    """
    Checks if cassandra service is running in given timeout
    :param cmd_helper:
    :param timeout: timeout in seconds to wait for cassandra service
    :param retry_interval: number of seconds to wait before each retry
    :return: True is cassandra service was found within given timeout
             False otherwise
    """
    timeout = time.time() + timeout
    while True:
        cmd_output = cmd_helper.run_cmd(command=CassandraConstants.SERVICE_STATUS_CMD, silent=True)
        if cmd_output and (cmd_output == CassandraConstants.SERVICE_RUNNING_OUTPUT):
            return True

        time.sleep(retry_interval)

        if time.time() > timeout:
            return False

    return False


def setup():
    logger = Logger(name="cassandra_setup")
    cmd_helper = Cmd_helper()

    if is_cassandra_running(cmd_helper=cmd_helper):
        logger.info("Cassandra service is running")
        cmd_helper.run_cmd(command=CassandraConstants.SERVICE_STOP_CMD)
        logger.info("Stopped cassandra service")

    # Load cassandra.yaml
    # Update seeds
    # Update listen_address, rpc_address, endpoint_snitch
    # Update auto_bootstrap: false
    # Update cluster_name
    # (future) Calculate num_tokens by using cores and memory
    # Update num_tokens to fixed value
    # Write update config to cassandra.yaml

    # Start cassandra service
    cmd_helper.run_cmd(command=CassandraConstants.SERVICE_START_CMD)
    if is_cassandra_running(cmd_helper=cmd_helper):
        logger.info("Cassandra service restarted successfully")
        time.sleep(10)

    with cassandra_client()as client:
        client.execute(CassandraConstants.CQL_CREATE_CEPH_KEYSPACE)
        client.set_keyspace(CassandraConstants.CEPH_DEFAULT_KEYSPACE)
        client.execute(CassandraConstants.CQL_CREATE_USER_TABLE)
        client.execute(CassandraConstants.CQL_CREATE_TASK_TABLE)

        # Get basic cluster info
        # Check nodetool status and validate peer node
        # Create keyspaces
        # Create tables
        pass
