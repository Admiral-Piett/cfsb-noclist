#!/bin/bash

PYTHON_VERSION=3.9.1
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

pyenv install --skip-existing ${PYTHON_VERSION}
rc=$?
if [[ ${rc} -ne 0 ]]; then
  echo "FAILURE - pyenv install --skip-existing ${PYTHON_VERSION}"
  exit 1
fi

pyenv local ${PYTHON_VERSION}
rc=$?
if [[ ${rc} -ne 0 ]]; then
  echo "FAILURE - pyenv local ${PYTHON_VERSION}"
  exit 1
fi

if ! command -v virtualenv &> /dev/null
then
    echo "installing virtualenv"

    pip install virtualenv
    rc=$?
    if [[ ${rc} -ne 0 ]]; then
      echo "FAILURE - pip install virtualenv"
      exit 1
    fi
fi

# Puts the virtual env in ./venv, and links to the python shim in pyenv.
virtualenv --python=$(pyenv which python) "${DIR}/venv"
rc=$?
if [[ ${rc} -ne 0 ]]; then
  echo "FAILURE - virtualenv --python=$(pyenv which python) ${DIR}/venv"
  exit 1
fi

echo "export PYTHONPATH=${PYTHONPATH}:${DIR}/src" >> ${DIR}/venv/bin/activate
. ${DIR}/venv/bin/activate

pip install -r requirements.txt
rc=$?
if [[ ${rc} -ne 0 ]]; then
  echo "FAILURE - pip install -r requirements.txt"
  exit 1
fi

echo "Install Success"
echo "Python location - $(which python)"
echo "Python location - $(python --version)"
