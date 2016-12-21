#!/bin/bash -e


isCassandraUp() {
    # Try to connect on Cassandra's JMX port 7199
    nc -z localhost 7199
    nc_return=$?

    # Try to connect on Cassandra CQLSH port 9042
    nc -z localhost 9042
    let "cassandra_status = nc_return + $?"

    retries=1
    while (( retries < 11 && cassandra_status != 0 )); do
        # Sleep for a while
        sleep 2s

        # Try again to connect to Cassandra
        nc -z localhost 7199
        nc_return=$?

        nc -z localhost 9042
        let "cassandra_status = nc_return + $?"

        let "retries++"
    done

    if [ ${cassandra_status} -ne 0 ]; then
        echo false
    else
        echo true
    fi
}

#cd /app

# Start the cassandra daemon
#cassandra
service cassandra start


if [ $(isCassandraUp) == true ]; then
    echo "Cassandra startup completed successfully --- OK"

    # Setup cassandra
    cassandra-utils/cassandra_utils.py -a setup --seed_source keepalived -l /var/log/

    # Create the schema
    # TODO move this to spring application (http://stackoverflow.com/questions/37352689/create-keyspace-table-and-generate-tables-dynamically-using-spring-data-cassanr)
    cqlsh -f /app/scripts/fiosceph.cql

    # Start spring boot application
    if [ "${BUILD_MODE}" == "dev" ]; then
        java -Xdebug -Xrunjdwp:transport=dt_socket,server=y,suspend=y,address=5005 -jar ceph-app.jar
    else
        java -jar ceph-app.jar
    fi
else
    echo "ERROR: Cassandra startup has ended with errors..."
fi
