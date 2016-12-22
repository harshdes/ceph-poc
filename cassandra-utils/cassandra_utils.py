#!/usr/bin/env python2.7
"""
TODO write basic intro about the module

"""
import argparse
import sys

from lib import cassandra_ops, ceph_ops, keepalived_ops
from lib.common_utils import do_global_config, Logger

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
    do_global_config(log_basedir=options.log_dir)
    logger = Logger(name="main")

    if options.action == "startup":
        logger.debug("Running startup sequence.")
        if not ceph_ops.is_monitor_node():
            logger.error("Current machine is not a CEPH monitor node. Exiting init sequence.")
            sys.exit(-2)

        monitor_nodes = ceph_ops.get_monitor_nodes()
        if not monitor_nodes:
            logger.error("Failed to find any CEPH monitor nodes to run management service. Exiting init sequence.")
            sys.exit(-3)

        logger.info("Found monitor nodes: {monitors}".format(monitors=monitor_nodes))

        # TODO add election code and remove hardcoded peer_node
        peer_node = monitor_nodes[1]

        logger.info("Node {peer} elected as peer for HA pair".format(peer=peer_node))

        # Setup cassandra on peer node
        # TODO

        # Setup keepalived on peer node
        # TODO

        # Setup cassandra on this node
        logger.debug("Running cassandra setup sequence.")
        cassandra_ops.setup(options.seeds)

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
