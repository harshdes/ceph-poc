'''
Created on Dec 20, 2016

@author: 25200
'''
from lib import cassandra_client
from lib.cassandra_client import cassandra_client
from lib.common_utils import Cmd_helper, Logger


def get_info():
    pass


def setup():
    logger = Logger()
    cmd_helper = Cmd_helper(logger=logger)
    # Stop cassandra service: sudo service cassandra stop
    cassandra_status = cmd_helper.run_cmd(command="service cassandra status")
    print "Cassandra status: ", cassandra_status

    # Load cassandra.yaml
    # Update seeds
    # Update listen_address, rpc_address, endpoint_snitch
    # Update auto_bootstrap: false
    # Update cluster_name
    # (future) Calculate num_tokens by using cores and memory
    # Update num_tokens to fixed value
    # Write update config to cassandra.yaml
    # Start cassandra service

    with cassandra_client()as client:
        # Get basic cluster info
        # Check nodetool status and validate peer node status
        pass
