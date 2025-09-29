import boto3
import uuid
import os
from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv

load_dotenv()  # Load AWS credentials from .env

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")

s3_client = boto3.client(
    "s3",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

def upload_to_s3(file, folder="lawyers"):
    """Upload a file to S3 and return its URL"""
    try:
        file_extension = file.filename.split(".")[-1]
        unique_filename = f"{folder}/{uuid.uuid4()}.{file_extension}"

        s3_client.upload_fileobj(
            file.file,
            AWS_BUCKET_NAME,
            unique_filename,
            ExtraArgs={"ContentType": file.content_type}   # ✅ removed ACL
        )

        # Build the public URL (works if bucket policy allows public read)
        file_url = f"https://{AWS_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{unique_filename}"
        return file_url

    except NoCredentialsError:
        raise Exception("AWS credentials not available")
