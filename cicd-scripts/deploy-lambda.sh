#!/bin/bash

set -e

BRANCH="main"

while [[ "$#" -gt 0 ]]; do
    case $1 in
        --branch) BRANCH="$2"; shift ;;
    esac
    shift
done

ROOT_DIR=$(pwd)
for LAMBDA_PATH in functions/*/
do
    if [ "$BRANCH" == "main" ]; then
        FUNCTION_NAME=$(basename $LAMBDA_PATH)
    else
        BRANCH_CLEANED="${BRANCH#feature/}"
        FUNCTION_NAME="$(basename $LAMBDA_PATH)-$BRANCH_CLEANED"
    fi

    echo "=== Start deploy-lambda $FUNCTION_NAME ==="
    
    cd $LAMBDA_PATH

    echo "Installing packages"
    mkdir package
    pip install --target package/ -r requirements.txt

    echo "Zipping functions"
    cd package
    if [ "$(find . -type d | grep -v '__pycache__' | wc -l)" -gt 1 ]; then
        zip -r ../lambda.zip . -x "*__pycache__*"
    else
        echo "No libraries to zip in the package directory."
    fi
    cd ..
    zip lambda.zip *.py

    echo "Deploying functions"
    aws lambda list-functions --profile localstack | jq '.Functions[].FunctionName' > lambda-list.txt
    if (cat lambda-list.txt | grep -q "\"$FUNCTION_NAME\""); then
        echo "Function $FUNCTION_NAME exists, updating function"
        aws lambda update-function-code \
            --profile localstack \
            --function-name $FUNCTION_NAME \
            --zip-file fileb://lambda.zip
    else
        echo "Function $FUNCTION_NAME doesn't exist, creating function"
        aws lambda create-function \
            --profile localstack \
            --function-name $FUNCTION_NAME \
            --runtime python3.10 \
            --role arn:aws:iam::000000000000:role/lambda-ex \
            --handler lambda_function.lambda_handler \
            --zip-file fileb://lambda.zip
    fi
    sleep 5

    echo "Updating environments"
    aws lambda update-function-configuration \
        --profile=localstack \
        --function-name $FUNCTION_NAME \
        --environment file://.env
    
    echo "=== End deploy-lambda $FUNCTION_NAME ==="

    cd $ROOT_DIR
done