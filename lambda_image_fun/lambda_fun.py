import boto3

s3 = boto3.client("s3")

# We do NOT need environment variable now — we know dest bucket name via code logic
DEST_BUCKET = "aleksandar-docker-dest-bucket"


def lambda_handler(event, context):
    """
    S3 trigger from 'aleksandar-docker-source-bucket'

    For every uploaded file:
      - read file from source bucket
      - write same content (no transform) to DEST_BUCKET
    """
    results = []

    for record in event["Records"]:
        source_bucket = record["s3"]["bucket"]["name"]  # should be aleksandar-docker-source-bucket
        source_key = record["s3"]["object"]["key"]

        # Read original file
        response = s3.get_object(Bucket=source_bucket, Key=source_key)
        body = response["Body"].read()

        # Write same file to destination bucket
        dest_key = source_key
        s3.put_object(Bucket=DEST_BUCKET, Key=dest_key, Body=body)

        results.append({
            "from": f"{source_bucket}/{source_key}",
            "to": f"{DEST_BUCKET}/{dest_key}"
        })

    return {"status": "OK", "copied": results}
