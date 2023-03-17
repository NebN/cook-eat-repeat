#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

source $SCRIPT_DIR/venv/bin/activate
cd $SCRIPT_DIR
gunicorn -b 0.0.0.0:5000 'src.api:app'
