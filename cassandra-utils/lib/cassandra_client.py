"""
Created on Dec 20, 2016

http://datastax.github.io/python-driver/api/cassandra/cluster.html
"""
from cassandra.cluster import Cluster


class cassandra_client(object):
    """
    classdocs
    """

    def __init__(self, address="localhost"):
        """
        Constructor
        :type address: String
        """
        self.address = address
        self.cluster = Cluster([self.address])

    def __enter__(self):
        # Create a cassandra cluster, connect and return it
        self.session = self.cluster.connect()
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
