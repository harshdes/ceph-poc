"""
Created on Jan 3, 2017
@author: Harsh Desai
"""


def is_monitor_node():
    """
    Checks if machine where the code runs is a ceph monitor node
    :return: True if machine is a ceph monitor mode, False otherwise
    """
    # TODO Add implementation. Invoke CEPH REST/CLI to check if node is monitor node
    return True


def get_monitor_nodes():
    """
    Fetches list of monitor nodes in ceph cluster
    :return: list of monitor nodes in ceph cluster
    """
    # TODO add implementation and remove hardcoded list
    return ["10.60.21.112"]

