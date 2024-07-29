# cicd-lambda

assumption:
- self hosted runner has localstack already installed ?
- iam role sudah setup, fixed
- aws profile fixed on runner host
- plus point: each function install only required library

zip: 
zip -r main.zip lambda_template/*.py lambda_template/package/*


aws iam create-role \
    --profile=localstack \
    --role-name lambda-ex \
    --assume-role-policy-document '{"Version": "2012-10-17","Statement": [{ "Effect": "Allow", "Principal": {"Service": "lambda.amazonaws.com"}, "Action": "sts:AssumeRole"}]}' 

create function:
aws lambda create-function \
    --profile localstack \
    --function-name lambda_template \
    --runtime python3.10 \
    --role arn:aws:iam::000000000000:role/lambda-ex \
    --handler lambda_function.lambda_handler \
    --zip-file fileb://main.zip

update function:
aws lambda update-function-code \
    --profile localstack \
    --function-name lambda_template \
    --zip-file fileb://main.zip

invoke:
aws lambda invoke \
    --profile=localstack \
    --function-name lambda_template \
    --payload '{}' \
    output.txt

aws lambda invoke \
    --profile=localstack \
    --function-name triangle_area \
    --payload file://payload.json \
    --cli-binary-format raw-in-base64-out \
    output.txt
aws lambda invoke \
    --profile=localstack \
    --function-name triangle_area \
    --payload '{ "base": 10, "height": 5 }' \
    --cli-binary-format raw-in-base64-out \
    output.txt


environment:

aws lambda update-function-configuration \
    --profile=localstack \
    --function-name triangle_area \
    --environment "Variables={COLOUR=BLUE}"

aws lambda update-function-configuration \
    --profile=localstack \
    --function-name triangle_area \
    --environment file://.env

aws lambda get-function-configuration \
    --profile=localstack \
    --function-name triangle_area



    