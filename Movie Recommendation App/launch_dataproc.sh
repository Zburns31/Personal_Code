#!/usr/bin/env bash

# ARGUMENTS:
# cluster_name n_workers git_branch_name datalake_version
#Set Script Name variable

SCRIPT=`basename ${BASH_SOURCE[0]}`
function usage()
{
    echo "this script will launch a dataproc cluster on GCP with pyspark support"
    echo "USAGE   : launch_dataproc.sh <cluster_name> <n_workers> <git_branch_name> <git_local_location> <datalake_version>"
    echo "EXAMPLE : ./launch_dataproc.sh cluster_sc_001 10 "
    echo ""
    echo "MANDATORY ARGUMENTS"
    echo "    <cluster_name>               -- name of the dataproc cluster to be created, must be unique"
    echo "    <n_workers>                  -- amount of worker nodes in the cluster"
    echo ""
}
if [ $# -lt 1 ]
then
	usage
	exit 1
fi
if [[ $1 == "-h" ||$1 == "--help" ]]
then
	usage
	exit 0
fi
# Parse arguments
CLUSTER_NAME=$1
N_WORKERS=$2
N_INSTANCES=$((2 * $N_WORKERS))
# SET VALUES
PROPERTIES="spark:spark.executor.cores=5,spark:spark.executor.memory=17G,spark:spark.executor.instances=${N_INSTANCES}"
INIT_TIMEOUT="30m"  
#TODO: add Datalab support
# INIT_ACTIONS=
# DERIVED VALUES
if [ -z ${INIT_ACTIONS} ]
    then
        STR_INIT_ACTIONS=""
    else
        STR_INIT_ACTIONS="--initialization-actions ${INIT_ACTIONS}"
fi
# Inform the user
echo "Creating cluster      [${CLUSTER_NAME}]"
echo "Image:                [${IMAGE_NAME}]"
echo "Init actions:         [${INIT_ACTIONS}]"
echo "Init timeout:         [${INIT_TIMEOUT}]"
# Do it
set -x
gcloud beta dataproc clusters create ${CLUSTER_NAME} \
    --region=us-central1 \
    --scopes cloud-platform \
    --image-version 1.4 \
    --optional-components=ANACONDA,JUPYTER \
    --enable-component-gateway \
    --master-machine-type=n1-standard-4 \
    --worker-machine-type=n1-standard-4 \
    --num-workers=${N_WORKERS} \
    --master-boot-disk-type=pd-ssd \
    --worker-boot-disk-type=pd-ssd \
    --num-master-local-ssds=1 \
    --num-worker-local-ssds=1 \
    --master-boot-disk-size=100 \
    --initialization-action-timeout ${INIT_TIMEOUT}  \
    --properties ${PROPERTIES}
set +x