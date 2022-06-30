import boto3
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.resource("s3")


def create_bucket(bucket_name, region):
    logger.info(f"Creating bucket {bucket_name}")

    bucket = s3.Bucket(bucket_name)
    if bucket.creation_date is None:
        bucket.create(CreateBucketConfiguration={"LocationConstraint": region})
    else:
        logger.info(f"Bucket {bucket_name} already exists")


def set_cors_policy(bucket_name, region, domain_id):
    logger.info(f"Setting CORS policy")

    bucket_cors = s3.BucketCors(bucket_name)
    bucket_cors.put(
        CORSConfiguration={
            "CORSRules": [
                {
                    "AllowedMethods": [
                        "POST",
                    ],
                    "AllowedOrigins": [
                        f"https://{domain_id}.studio.{region}.sagemaker.aws",
                    ],
                    "ExposeHeaders": [],
                },
            ]
        }
    )


def lambda_handler(event, context):
    account_id = context.invoked_function_arn.split(":")[4]
    region = os.environ["AWS_REGION"]
    domain_id = os.environ["DOMAIN_ID"]
    domain_id = "toto"

    bucket_name = f"sagemaker-{region}-{account_id}"

    try:
        create_bucket(bucket_name, region)
        set_cors_policy(bucket_name, region, domain_id)
        logger.info("CORS policy set for Canvas bucket")
    except Exception as e:
        logger.error(e)
