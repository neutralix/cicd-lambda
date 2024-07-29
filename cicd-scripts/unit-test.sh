#!/bin/bash

set -e

ROOT_DIR=$(pwd)
for LAMBDA_PATH in functions/*/
do
    FUNCTION_NAME=$(basename $LAMBDA_PATH)
    echo "=== Start unit-test $FUNCTION_NAME ==="

    cd functions/$FUNCTION_NAME

    echo "Installing packages"
    mkdir package
    pip install --target package/ -r requirements.txt

    echo "Run unit-test"
    cd ..
    python -m unittest discover -s $FUNCTION_NAME/tests/

    echo "=== End unit-test $FUNCTION_NAME ==="

    cd $ROOT_DIR
done