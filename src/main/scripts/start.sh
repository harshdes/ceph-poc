#!/bin/bash -e


if [ "${NODE_MODE}" == "active" ]; then
    # Setup cassandra
    apis-utils/apis-utils.py -a startup -l /var/log/

    if [ "${BUILD_MODE}" == "dev" ]; then
        java -Xdebug -Xrunjdwp:transport=dt_socket,server=y,suspend=y,address=5005 -jar ceph-app.jar &
    else
        java -jar ceph-app.jar &
    fi
fi

tail -f /dev/null