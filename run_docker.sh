#!/bin/bash

usage() { echo "Usage: $0 [-f <container_image_file>] [-i <image_id_or_name>] [-n <container_name>]" 1>&2; exit 1; }

##### Check docker access #####
docker ps >/dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "Error: Please run this script from a terminal that has access to docker functionality"
    exit -1
fi

##### Parse args #####
while getopts ":f:i::n:" o; do
    case "${o}" in
        f)
            f=${OPTARG}
            ;;
        i)
            i=${OPTARG}
            ;;
        n)
            n=${OPTARG}
            ;;
        *)
            usage
            ;;
    esac
done
shift $((OPTIND-1))

if [ -z "${f}" ] && [ -z "${i}" ]; then
    echo "Either container image ID/Name or container image tar file must be specified."
    usage
fi

IMAGE_FILE=${f}
IMAGE_NAME=${i}
CONTAINER_NAME=${n:-ceph}

isDockerToolbox() {
    which docker-machine > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo true
        return
    fi

    echo false
}

isCephImage() {
    image=$1
    company=`docker inspect --format='{{json .Config.Labels.company}}' $image 2>/dev/null`
    product=`docker inspect --format='{{json .Config.Labels.product}}' $image 2>/dev/null`
    if { [ "$company" == "\"WesternDigitialCorp\"" ] && [ "$product" == "\"ceph\"" ]; }; then
        echo true
        return
    fi

    echo false
}

##### Get and validate container image #####
if [[ ${IMAGE_FILE} ]]; then
    if [ -e ${IMAGE_FILE} ]; then
        echo "Using image file  ${IMAGE_FILE} to create container..."
        docker_load_output=`docker load -i ${IMAGE_FILE}`
        OLD_IFS=$IFS
        IFS=':'
        arr=(${docker_load_output})
        IFS=$OLD_IFS
        export IMAGE_NAME=${arr[2]}
        if [ -z "${IMAGE_NAME}" ]; then
            echo "Error: Failed to load container image file"
            exit -1
        fi
    else
        echo "Error: given container image file '${IMAGE_FILE}' does not exist."
    fi
fi

if [ $(isCephImage ${IMAGE_NAME}) == false ]; then
    echo "Given image ${IMAGE_NAME} is not a FlashSoft container..."
    exit -1
fi

##### Stop previous conflicting containers #####
echo "Using image ${IMAGE_NAME} to create container..."
if [[ $(docker ps -a -q -f name=^/${CONTAINER_NAME}$) ]]; then
    echo "Stopping previous '${CONTAINER_NAME}' container since it conflicts with requested name"
    docker stop ${CONTAINER_NAME} > /dev/null
    echo "Renaming previous '${CONTAINER_NAME}' container to '${CONTAINER_NAME}.old'"
    if [[ $(docker ps -a -q -f name=^/${CONTAINER_NAME}.old$) ]]; then
        docker stop ${CONTAINER_NAME}.old > /dev/null; docker rm ${CONTAINER_NAME}.old > /dev/null
    fi
    docker rename ${CONTAINER_NAME} ${CONTAINER_NAME}.old > /dev/null
fi

##### Run container #####
echo "Starting ${CONTAINER_NAME} container"

if [[ ${CONTAINER_NAME} ]]; then
    NAME_ARGUMENT=" --name ${CONTAINER_NAME} "
fi

MEM_SETTINGS="-m 2g --memory-swap=2g"
new_container=`docker run -td  ${MEM_SETTINGS} -p 80:8080 ${NAME_ARGUMENT} ${IMAGE_NAME}`
if [[ $? -eq 0 ]]; then
    echo "Successfully started container with ID: ${new_container}"
    HOST_PORT_8080=`docker inspect --format='{{(index (index .NetworkSettings.Ports "8080/tcp") 0).HostPort}}' ${new_container}`
    if [ $(isDockerToolbox) == true ]; then
        export WEB_URL="http://`docker-machine ip`:${HOST_PORT_8080}"
    else
        export WEB_URL="http://`hostname -f`:${HOST_PORT_8080}"
    fi

    echo -e "After few seconds of startup time, the application can be accessed at: \033[1m ${WEB_URL}\033[0m"
else
    echo "Failed to start container using image ${IMAGE_NAME}"
    echo "Please ensure you stop any previously running container for this product."
fi