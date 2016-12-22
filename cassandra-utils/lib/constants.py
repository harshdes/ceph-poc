"""

"""


class CassandraConstants(object):
    """
    Class to save constant cassandra related constants
    """
    # Commands
    SERVICE_START_CMD = "service cassandra start"
    SERVICE_STOP_CMD = "service cassandra stop"
    SERVICE_STATUS_CMD = "service cassandra status"

    # Common outputs
    SERVICE_RUNNING_OUTPUT = "Cassandra is running."
    SERVICE_NOT_RUNNING_OUTPUT = "Cassandra is not running."

    # Cassandra cluster properties
    CEPH_DEFAULT_KEYSPACE = "fiosceph"
    REPLICATION_STRATEGY="SimpleStrategy"
    REPLICATION_FACTOR = 1

    # CQL queries
    CQL_CREATE_CEPH_KEYSPACE = "CREATE KEYSPACE IF NOT EXISTS {keyspace} WITH replication={{'class':'{rep_strategy}', "\
                               "'replication_factor': {rep_factor}}}; ".format(keyspace=CEPH_DEFAULT_KEYSPACE,
                                                                               rep_strategy=REPLICATION_STRATEGY,
                                                                               rep_factor=REPLICATION_FACTOR)
    CQL_CREATE_USER_TABLE = "CREATE TABLE IF NOT EXISTS users (name text PRIMARY KEY, password text, " \
                            " emails set<text>); "
    CQL_CREATE_TASK_TABLE = "CREATE TABLE IF NOT EXISTS tasks (id text PRIMARY KEY, state text);"
