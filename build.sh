#!/bin/bash -e
./mvnw clean package

docker build -t ceph .
./run_docker.sh -i ceph
#docker stop ceph
#docker rm ceph
#docker run -td -p 80:8080 --name=ceph ceph