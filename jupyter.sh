#!/usr/bin/env bash
set -eu

source .venv/bin/activate

# jupyter nbextension install jupyter_ascending --user --py && \
# jupyter nbextension enable jupyter_ascending --user --py && \
# jupyter serverextension enable jupyter_ascending --user --py

jt -t chesterish

jupyter notebook --ip 0.0.0.0
