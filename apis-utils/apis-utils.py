#!/usr/bin/env python2.7
"""
TODO write basic intro about the module

"""
import argparse
import logging.config
import random
import socket
import sys

from lib import cassandra_ops, ceph_ops, keepalived_ops
from lib.common_utils import CmdHelper, setup_logging

__author__ = "Harsh Desai"
__maintainer__ = "Harsh Desai"
__email__ = "Harsh.Desai@SanDisk.com"


def get_args():
    parser = argparse.ArgumentParser(description='This is a utilty module for cassandra_client bringup')
    parser.add_argument("-a", "--action", help='Provide the action to perform', choices=["startup", "cassandra_setup",
                                                                                         "keepalived_setup"],
                        required=True)
    parser.add_argument("-s", "--seeds", nargs="*", help='Provider white-space seperated list of seeds', required=False)

    parser.add_argument("-l", "--log_dir", help="Location of logs directory", default="/tmp/", required=False)
    return parser.parse_args()


if __name__ == '__main__':
    options = get_args()
    setup_logging()
    logger = logging.getLogger(__name__)
    cmd_helper = CmdHelper()

    if options.action == "startup":
        logger.debug("Running startup sequence.")
        if not ceph_ops.is_monitor_node():
            logger.error("Current machine is not a CEPH monitor node. Exiting init sequence.")
            sys.exit(-2)

        # Get possible candidates for the peer node
        monitor_nodes = ceph_ops.get_monitor_nodes()
        if not monitor_nodes:
            logger.error("Failed to find any CEPH monitor nodes to run management service. Exiting init sequence.")
            sys.exit(-3)

        # Remove the executing node
        if str(socket.gethostbyname(socket.gethostname())) in monitor_nodes:
            monitor_nodes.remove(str(socket.gethostbyname(socket.gethostname())))

        logger.info("Found monitor nodes: {monitors}".format(monitors=monitor_nodes))

        # Randomly select a peer node
        peer_node = monitor_nodes[random.randrange(len(monitor_nodes))]

        logger.info("Node {peer} elected as peer for HA pair".format(peer=peer_node))

        # Setup cassandra on peer node
        cmd = "docker exec ceph /app/apis-utils/apis-utils.py -a cassandra_setup -l /var/log/ -s " + \
              "127.0.0.1 " + str(socket.gethostbyname(socket.gethostname()))
        cmd_helper.run_remote_cmd(cmd=cmd, host=peer_node, host_user="root", host_password="Flash123")

        # # Setup keepalived on peer node
        # cmd = "docker exec ceph /app/apis-utils/apis-utils.py -a keepalived_setup -l /var/log/"
        # cmd_helper.run_remote_cmd(cmd=cmd, host=peer_node, host_user="root", host_password="Flash123")

        # Setup cassandra on this node
        logger.debug("Running cassandra setup sequence.")
        seeds = ['127.0.0.1', peer_node]
        cassandra_ops.setup(seeds)

        # Setup keepalived on this node
        logger.debug("Running keepalived setup sequence.")
        keepalived_ops.setup()

        # Start springboot
        # TODO
    elif options.action == "cassandra_setup":
        logger.debug("Running cassandra setup sequence.")
        cassandra_ops.setup(options.seeds)
    elif options.action == "keepalived_setup":
        logger.debug("Running keepalived setup sequence.")
        keepalived_ops.setup()
    else:
        logger.error("[ERROR] Unsupported action invoked: " + options.action)
        sys.exit(-1)
