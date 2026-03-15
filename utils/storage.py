import os
from config.storage import get_s3_client

def upload_file(file_bytes: bytes, filename: str, content_type: str) -> str:
    client = get_s3_client()
    bucket = os.environ["B2_BUCKET_NAME"]

    client.put_object(
        Bucket=bucket,
        Key=filename,
        Body=file_bytes,
        ContentType=content_type
    )


    endpoint = os.environ["B2_ENDPOINT_URL"]
    return f"{endpoint}/file/{bucket}/{filename}"


def delete_file(filename: str) -> None:
    client = get_s3_client()
    client.delete_object(
        Bucket=os.environ["B2_BUCKET_NAME"],
        Key=filename
    )


def get_signed_url(filename: str, expires_in: int = 3600) -> str:

    client = get_s3_client()
    return client.generate_presigned_url(
        "get_object",
        Params={
            "Bucket": os.environ["B2_BUCKET_NAME"],
            "Key": filename
        },
        ExpiresIn=expires_in
    )