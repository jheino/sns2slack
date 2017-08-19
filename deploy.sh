#!/bin/sh

aws cloudformation package \
	--template-file sns2slack.yaml \
	--s3-bucket jheino-lambda \
	--output-template-file sns2slack-output.yaml

aws cloudformation deploy \
	--template-file sns2slack-output.yaml \
	--stack-name SNS2Slack \
	--capabilities CAPABILITY_IAM \
	--parameter-overrides WebhookUrl=https://hooks.slack.com/services/...
