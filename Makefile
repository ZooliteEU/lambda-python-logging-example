.PHONY: clean install uninstall lint test build package deploy
.DEFAULT_GOAL:=help

# Variables
S3_BUCKET=lambda-source-440357826049
S3_PREFIX=zoolite-serverless-demo
CFN_TEMPLATE=cfn-template.yaml
CFN_TEMPLATE_OUT=cfn-template-out.yaml
CFN_STACK_NAME=zoolite-serverless-demo
AWS_REGION=eu-west-1


package:  ## Package Lambda function and SAM template
	sam package --template-file $(CFN_TEMPLATE) --s3-bucket $(S3_BUCKET) --s3-prefix $(S3_PREFIX) --output-template-file $(CFN_TEMPLATE_OUT)

deploy: package  ## Deploy SAM template
	sam deploy --stack-name $(CFN_STACK_NAME) --template-file $(CFN_TEMPLATE_OUT) --capabilities CAPABILITY_NAMED_IAM --region $(AWS_REGION)

help:
	$(call blue, "Help:\n=====")
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m- %-20s\033[0m %s\n",$$1, $$2}'


define blue
	@tput setaf 10
	@echo $1
	@tput sgr0
endef

