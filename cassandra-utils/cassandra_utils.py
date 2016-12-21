#!/usr/bin/env python2.7
"""
TODO write basic intro about the module

"""
import argparse
import sys

from lib import operations
from lib.common_utils import do_global_config

__author__ = "Harsh Desai"
__maintainer__ = "Harsh Desai"
__email__ = "Harsh.Desai@SanDisk.com"


def get_args():
    parser = argparse.ArgumentParser(description='This is a utilty module for cassandra_client bringup')
    parser.add_argument("-a", "--action", help='Provide the action to perform', choices=["getinfo", "setup"],
                        required=True)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-s", "--seeds", nargs="*", help='Provider white-space seperated list of seeds', required=False)
    group.add_argument("--seed_source", help="Informs from where to pick the seed list for cassandra_client",
                       choices=["keepalived"])

    parser.add_argument("-l", "--log_dir", help="Location of logs directory", default="/tmp/", required=False)
    return parser.parse_args()


if __name__ == '__main__':
    options = get_args()
    do_global_config(log_basedir=options.log_dir)

    if options.action == "getinfo":
        operations.get_info()
    elif options.action == "setup":
        operations.setup()
    else:
        print "[ERROR] Unsupported action invokd: " + options.action
        sys.exit(-1)
