"""
Created on Dec 20, 2016

@author: 25200
"""
import datetime
import shutil

import os

from lib import cassandra_client
from lib.cassandra_client import cassandra_client
from lib.common_utils import CmdHelper, Logger, netcat, read_yaml_file, write_yaml_file
from lib.constants import CassandraConstants
import time


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
        # Also check if cassandra is listening on jmx and cqlsh ports since even after service being up, there is a
        # delay in the service listening on those ports
        if cmd_output and (cmd_output == CassandraConstants.SERVICE_RUNNING_OUTPUT) and \
                netcat(hostname=CassandraConstants.CLUSTER_ADDRESS, port=CassandraConstants.CASSANDRA_JMX_PORT) and \
                netcat(hostname=CassandraConstants.CLUSTER_ADDRESS, port=CassandraConstants.CASSANDRA_CQLSH_PORT):
            return True

        time.sleep(retry_interval)

        if time.time() > timeout:
            return False

    return False


def setup(seeds=None):
    logger = Logger(name="cassandra_setup")
    cmd_helper = CmdHelper()

    cmd_helper.run_cmd(command=CassandraConstants.SERVICE_STOP_CMD, silent=True)

    # Load cassandra.yaml
    config = read_yaml_file(CassandraConstants.CASSANDRA_CONFIG_FILE)
    logger.debug("cassandra config before edit: {cfg}".format(cfg=config))

    # Update seeds
    # (optional) Update listen_address, rpc_address, endpoint_snitch

    # Update cluster_name
    config['cluster_name'] = CassandraConstants.CEPH_CLUSTER_NAME

    # (future) Calculate num_tokens by using cores and memory of current machine

    # Backup existing file before modifying it
    modified_time = os.path.getmtime(CassandraConstants.CASSANDRA_CONFIG_FILE)
    timestamp = datetime.datetime.fromtimestamp(modified_time).strftime("%b-%d-%y-%H:%M:%S")

    shutil.copy(CassandraConstants.CASSANDRA_CONFIG_FILE,
                CassandraConstants.CASSANDRA_CONFIG_FILE + ".bkp." + timestamp)

    # Write update config to cassandra.yaml
    write_yaml_file(CassandraConstants.CASSANDRA_CONFIG_FILE, config)

    # Start cassandra service
    cmd_helper.run_cmd(command=CassandraConstants.SERVICE_START_CMD)
    if is_cassandra_running(cmd_helper=cmd_helper):
        logger.info("Cassandra service started successfully")

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
