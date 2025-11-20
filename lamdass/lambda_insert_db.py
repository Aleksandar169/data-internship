import json
import os
import logging
import boto3

TABLE_NAME = os.environ["DYNAMODB_TABLE_NAME"]

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ALLOWED_PREFIXES = ("pollution/", "sensor/", "weather/")


def lambda_handler(event, context):
    for sqs_record in event["Records"]:
        body = sqs_record["body"]

        try:
            s3_event = json.loads(body)
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON in SQS message: {body}")
            continue

        for s3_record in s3_event.get("Records", []):
            bucket = s3_record["s3"]["bucket"]["name"]
            key = s3_record["s3"]["object"]["key"]

            if not key.startswith(ALLOWED_PREFIXES):
                logger.info(f"Ignored file: s3://{bucket}/{key}")
                continue

            timestamp = s3_record.get("eventTime", "UNKNOWN")

            item = {
                "file_name": key,
                "timestamp": timestamp,
                "status": 0
            }

            table.put_item(Item=item)
            logger.info(f"Inserted into DynamoDB: {item}")

    return {"statusCode": 200}
