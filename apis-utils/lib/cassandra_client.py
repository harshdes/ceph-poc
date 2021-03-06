"""
Created on Dec 20, 2016

http://datastax.github.io/python-driver/api/cassandra/cluster.html
"""
import logging
from cassandra.cluster import Cluster

from lib.constants import CassandraConstants


class cassandra_client(object):
    """
    classdocs
    """

    def __init__(self, address=CassandraConstants.CLUSTER_ADDRESS, keyspace=CassandraConstants.CEPH_DEFAULT_KEYSPACE):
        """
        Constructor
        """
        self.keyspace = keyspace
        self.address = address
        self.cluster = Cluster(contact_points=[self.address])
        self.logger = logging.getLogger(__name__)

    def __enter__(self):
        self.session = self.cluster.connect()
        self.logger.info("Successfully connected to cluster")
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        """ Closes all sessions and connection associated with this Cluster.
            Once shutdown, a Cluster should not be used for any purpose.
            Used automatically through Python's "with" keyword.

        Parameters are standard:

        :param exc_type: exception type, if any, seen
        :type exc_type: type
        :param exc_val: exception seen
        :type exc_val: Exception
        :param exc_tb: traceback related to the exception
        :type exc_tb: traceback
        """
        self.cluster.shutdown()
