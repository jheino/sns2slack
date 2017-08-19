# sns2slack

sns2slack is a Lambda function for publishing SNS messages in Slack using an
incoming webhook. It is built using the [AWS Serverless Application
Model](https://github.com/awslabs/serverless-application-model).

## Requirements

You need to have a working AWS CLI setup.

## Usage

1. Create an S3 bucket for storing the Lambda function
2. Create a Slack incoming webhook
3. Edit `deploy.sh` and set `S3_BUCKET` and `WEBHOOK_URL` accordingly
4. Run `./deploy.sh`
5. An SNS topic will be created which will deliver all published messages to
   your Slack webhook.
