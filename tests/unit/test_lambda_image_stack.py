import aws_cdk as core
import aws_cdk.assertions as assertions

from lambda_image.lambda_image_stack import LambdaImageStack

# example tests. To run these tests, uncomment this file along with the example
# resource in lambda_image/lambda_image_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = LambdaImageStack(app, "lambda-image")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
