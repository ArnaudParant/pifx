#!/bin/bash

export PYTHONPATH=${PYTHONPATH}:/src

if [ "${HOST}" == "" ]; then HOST="0.0.0.0"; fi
if [ "${PORT}" == "" ]; then PORT="9100"; fi

python -m pifx.routes "${HOST}" "${PORT}"
