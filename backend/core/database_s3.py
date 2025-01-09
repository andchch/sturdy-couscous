from uuid import uuid4
import boto3
from fastapi import UploadFile

from backend.core.config import get_s3_creds

s3_client = boto3.client(
    service_name='s3', endpoint_url=f'https://{get_s3_creds()[3]}',
    aws_access_key_id=f'{get_s3_creds()[0]}:{get_s3_creds()[1]}',
    aws_secret_access_key=get_s3_creds()[2],
    region_name='ru-central-1'
)

def upload_file_to_s3(file: UploadFile, bucket: str) -> str:
    unique_filename = f'{uuid4().hex}_{file.filename}'
    s3_client.upload_fileobj(
        file.file,
        bucket,
        unique_filename,
        ExtraArgs={"ContentType": file.content_type, "ACL": "public-read"},
    )
    file_url = f'https://{get_s3_creds()[3]}/{bucket}/{unique_filename}'
    return file_url

def get_user_avatar(name: str) -> str:
    # Generate the S3 presigned URL
    s3_presigned_url = s3_client.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': 'user.media',
            'Key': f'{name}'
        },
        ExpiresIn=3600 # 1 hour
    )
    return s3_presigned_url
