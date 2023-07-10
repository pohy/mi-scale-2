#!/usr/bin/env bash

if [ ${EUID} -ne 0 ]
then
	echo "root required"
	exit 1
fi

# Start the server
cd /home/pohy/mi-scale-2
./venv/bin/activate
ENV=production python ./main.py