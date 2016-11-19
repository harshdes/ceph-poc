#!/bin/bash


isCassandraUp() {
    # Try to connect on Cassandra's JMX port 7199
    nc -z localhost 7199
    nc_return=$?

    # Try to connect on Cassandra CQLSH port 9042
    nc -z localhost 9042
    let "cassandra_status = nc_return + $?"

    retries=1
    while (( retries < 6 && cassandra_status != 0 )); do
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

cassandra

if [ $(isCassandraUp) == true ]; then
    echo "Cassandra startup completed successfully --- OK"
    cqlsh -f /app/scripts/fiosceph.cql

    cd /app
    java -jar ceph-app.jar
else
    echo "ERROR: Cassandra startup has ended with errors..."
fi
