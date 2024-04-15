# AWS-Lambda

The S3 Object Mover Lambda Function is designed to automatically move objects from a source S3 bucket to a destination bucket based on predefined rules. This README provides instructions for setting up and using the Lambda function.

**Prerequisites**

AWS account with appropriate permissions to create Lambda functions and S3 buckets.
AWS CLI installed and configured with access keys and default region.
Setup Instructions
Clone Repository: Clone this repository to your local machine.

```bash
git clone https://github.com/Rohit3Pandey/AWS-Lambda.git
```
Navigate to Project Directory: Change to the project directory.

```bash
cd s3-object-mover-lambda
```
Install Dependencies: Install the required Python dependencies using pip.

```bash
pip install boto3
```
Configure AWS Credentials: Ensure that your AWS credentials are properly configured either through the AWS CLI or environment variables.

```bash
aws configure
```
Create IAM Role: Create an IAM role with permissions to access S3 and CloudWatch logs. Replace YourRoleName with a suitable name for your role.

```bash
aws iam create-role --role-name YourRoleName --assume-role-policy-document file://trust-policy.json
```
Attach Policies: Attach the necessary policies to the IAM role created in the previous step. Replace YourRoleARN with the ARN of your IAM role.
```bash
aws iam attach-role-policy --role-name YourRoleName --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
aws iam attach-role-policy --role-name YourRoleName --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess
```
Deploy Lambda Function: Deploy the Lambda function using the AWS CLI. Replace YourFunctionName with a suitable name for your Lambda function.

```bash
aws lambda create-function --function-name YourFunctionName --runtime python3.8 --role YourRoleARN --handler lambda_function.lambda_handler --zip-file fileb://lambda_function.zip
```
Create S3 Buckets: Create the source and destination S3 buckets. Replace source-bucket-name and destination-bucket-name with your desired bucket names.

```bash
aws s3 mb s3://source-bucket-name
aws s3 mb s3://destination-bucket-name
```
Configure S3 Event: Configure the source bucket to trigger the Lambda function on object creation events.

```bash
aws s3api put-bucket-notification-configuration --bucket source-bucket-name --notification-configuration file://notification-config.json
```
**Usage**

Upload Files: Upload files to the source S3 bucket. The Lambda function will automatically move them to the destination bucket based on file extension.

Monitor Logs: Monitor the CloudWatch logs for the Lambda function to view execution logs and track object movement.

**Troubleshooting**

If the Lambda function fails to execute or encounters errors, check the CloudWatch logs for detailed error messages and debugging information.

Ensure that the IAM role attached to the Lambda function has sufficient permissions to access S3 buckets and CloudWatch logs.

Verify that the source and destination S3 buckets are correctly configured and accessible.
