import boto3
import os
from botocore.client import Config

def get_s3_client():
    return boto3.client(
        "s3",
        endpoint_url=os.environ["B2_ENDPOINT_URL"],         
        aws_access_key_id=os.environ["B2_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["B2_SECRET_ACCESS_KEY"],
        config=Config(signature_version="s3v4")
    )