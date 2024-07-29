# GitHub Actions CI/CD for AWS Lambda

## Overview
This document provides information about the CI/CD for deploying AWS Lambda functions on a monorepo. The CI/CD is managed using GitHub Actions workflow and involves several stages from lint test, unit test, and lambda deployment.

Monorepo structure:
```
.
└── functions/
    ├── lambda_template/                    <--- root directory for a lambda function
    │   ├── tests/                          <--- put all unit test code here
    │   │   └── test_lambda_function.py
    │   ├── __init__.py
    │   ├── .env                            <--- modify environment for lambda function
    │   ├── .pylintrc                       <--- modify lint test configuration
    │   ├── lambda_function.py
    │   └── requirements.txt                <--- put all dependency here
    ├── (add new function here)
    ├── (add new function here)
    └── (add new function here)
```

Lambda function is run using `Python 3.10` and `x64` architecture. To initiate a new function, please copy `lambda_template` directory. From there you can modify your lambda function code, along with unit test function under `tests/` directory.  
This CI/CD handle Python library depedency installation. List out library name on `requirements.txt` file.  
To modify lambda function environment, modify your environment on `.env` file.  
Lint test can be configured as needed on `.pylintrc` file.  

## CI/CD Flow Diagram
[Insert Flow Diagram Here]

## Assumptions
- GitHub repository has a self-hosted runner set up.
- Docker and LocalStack are used to simulate local AWS.
- AWS CLI on CI/CD has been statically configured for LocalStack.
- CI/CD will push lambda code with fixed pre-created AWS IAM Role and handler.

## Branching Strategy
- Master branch  
Branch name pattern: **`main`**  
Main branch of the repository. This branch holds the stable and production-ready code.  
CI/CD will run on commit to this branch to push all lambda function under functions directory.  
Pushed function will have function name according to their directory name.  
Function on directory **`example`** will have function name **`example`**.  
- Development Branch  
Branch name pattern : **`feature/*`**  
Feature branch for development purpose. This branch could be used for developing new features, bug fixes, or other changes.  
CI/CD will also run on commit to this branch to push all lambda function under functions directory.  
Pushed function will have function name according to their directory name, with added suffix of the branch name.  
Function on directory **`example`** on **`feature/test`** will have function name **`example-test`**.  
- Flexible Branch  
Branch name pattern : **`*`**  
Free branch for any purpose. CI/CD will not run on this branch. This branch could be used to work that doesn't require immediate lambda function push.  

## Documentation
I set up a self-hosted runner to help myself get quicker feedback on developing this CI/CD.  

![](images/runner.jpg)


## Limitation & Improvement
a
