#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

source $SCRIPT_DIR/venv/bin/activate
cd $SCRIPT_DIR
gunicorn 'src.api:app'
