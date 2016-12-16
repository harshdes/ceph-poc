#!/bin/bash -e

# Take BUILD_MODE from environment if specified, else default to false
BUILD_MODE=${BUILD_MODE:-"prod"}

usage() { echo "Usage: $0 [-b] [-h]" 1>&2; exit 1; }

args=`getopt hb: $*`

# Rewrite ARGV with the output of getopt
set -- $args

# i refers to each positional parameter
for i do
  case "$i" in
    -b)
      BUILD_MODE=$2;
      # Remove the current option from ARGV so that the next one is
      # available
      shift;;
    -h)
      usage
      shift; break;;
    --)
      shift; break;;
  esac
done

# Build the java application
./mvnw clean package

# Build the docker container
docker build -t ceph .

# Run the container
./run_docker.sh -i ceph -b ${BUILD_MODE}