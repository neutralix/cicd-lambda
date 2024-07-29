#!/bin/bash

ROOT_DIR=$(pwd)
for LAMBDA_PATH in functions/*/
do
    FUNCTION_NAME=$(basename $LAMBDA_PATH)
    echo "=== Start lint-test $FUNCTION_NAME ==="

    cd functions/$FUNCTION_NAME

    echo "Installing packages"
    mkdir package
    pip install --target package/ -r requirements.txt

    echo "Run lint-test"
    pylint . --rcfile=.pylintrc
    python -m json.tool .env > /dev/null

    echo "=== End lint-test $FUNCTION_NAME ==="
    
    cd $ROOT_DIR
done