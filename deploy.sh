#!/bin/sh

S3_BUCKET=
WEBHOOK_URL=

aws cloudformation package \
	--template-file sns2slack.yaml \
	--s3-bucket ${S3_BUCKET} \
	--output-template-file sns2slack-output.yaml

aws cloudformation deploy \
	--template-file sns2slack-output.yaml \
	--stack-name SNS2Slack \
	--capabilities CAPABILITY_IAM \
	--parameter-overrides WebhookUrl=${WEBHOOK_URL}
