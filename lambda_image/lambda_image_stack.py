from constructs import Construct
import aws_cdk as cdk
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_s3 as s3,
    aws_s3_notifications as s3n,
)


class LambdaStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # 1) Create new buckets in AWS

        source_bucket = s3.Bucket(
            self,
            "SourceBucket",
            bucket_name="aleksandar-docker-source-bucket",
            removal_policy=cdk.RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )

        dest_bucket = s3.Bucket(
            self,
            "DestBucket",
            bucket_name="aleksandar-docker-dest-bucket",
            removal_policy=cdk.RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )

        # 2) Create Docker image Lambda function

        copy_function = _lambda.DockerImageFunction(
            self,
            "CopyCSVFunction",
            code=_lambda.DockerImageCode.from_image_asset(
                directory="lambda_image_fun"
            ),
            timeout=cdk.Duration.seconds(30),
            memory_size=256,
        )

        # Permissions for Lambda
        source_bucket.grant_read(copy_function)
        dest_bucket.grant_write(copy_function)

        #  Trigger on upload (*.csv)
        source_bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED,
            s3n.LambdaDestination(copy_function),
            # s3.NotificationKeyFilter(suffix=".csv")
        )

        extra_layer = _lambda.LayerVersion(
            self,
            "ExtraLibLayer",
            code=_lambda.Code.from_asset("layer"),
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_11],
            description="Layer with extra_lib (shout function)",
        )

        layered_lambda = _lambda.Function(
            self,
            "LayeredLambdaFunction",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="lambda_layer_fun.lambda_handler",
            code=_lambda.Code.from_asset("layer_lambda"),
            layers=[extra_layer],
        )
