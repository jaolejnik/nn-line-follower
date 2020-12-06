#!/bin/bash

REMOTE_USER="pi"
IP_ADDRESS="192.168.1.${1}"
WORKDIR_PATH="~/nn-line-follower/"

ssh "${REMOTE_USER}@${IP_ADDRESS}" "rm -rf ${WORKDIR_PATH}"
ssh "${REMOTE_USER}@${IP_ADDRESS}" "mkdir -p ${WORKDIR_PATH}"
ssh "${REMOTE_USER}@${IP_ADDRESS}" "mkdir -p ${WORKDIR_PATH}/utils"
echo "${FILES_TO_COPY} ${REMOTE_USER}@${IP_ADDRESS}:${WORKDIR_PATH}"
scp -r  robot/ saved_data/interesting_models/G188_METAAAAA converted_model.tflite Pipfile* rpi_main.py "${REMOTE_USER}@${IP_ADDRESS}:${WORKDIR_PATH}"
scp -r  utils/enums.py  utils/timer.py "${REMOTE_USER}@${IP_ADDRESS}:${WORKDIR_PATH}/utils"


