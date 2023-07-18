#!/usr/bin/env bash

if [ ${EUID} -ne 0 ]
then
	echo "root required"
	exit 1
fi

# Start the server
# TODO: I don't think that an absolute path is necessary :)
cd /home/pohy/mi-scale-2
.venv/bin/activate
ENV=production python -m mi_scale_2.main
