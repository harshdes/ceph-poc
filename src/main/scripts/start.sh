#!/bin/bash -e

# Setup cassandra
cassandra-utils/cassandra_utils.py -a startup -l /var/log/

# Start spring boot application
if [ "${BUILD_MODE}" == "dev" ]; then
    java -Xdebug -Xrunjdwp:transport=dt_socket,server=y,suspend=y,address=5005 -jar ceph-app.jar
else
    java -jar ceph-app.jar
fi
