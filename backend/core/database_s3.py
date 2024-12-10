from uuid import uuid4
import boto3
from fastapi import UploadFile

from backend.core.config import get_s3_creds

S3_MEDIA_BUCKET='bucket-913415'

s3_client = boto3.client(
    service_name='s3', endpoint_url=f'https://{get_s3_creds()[3]}',
    aws_access_key_id=f'{get_s3_creds()[0]}:{get_s3_creds()[1]}',
    aws_secret_access_key=get_s3_creds()[2],
    region_name='ru-central-1'
)

def upload_file_to_s3(file: UploadFile) -> str:
    unique_filename = f'{uuid4().hex}_{file.filename}'
    s3_client.upload_fileobj(
        file.file,
        S3_MEDIA_BUCKET,
        unique_filename,
        ExtraArgs={"ContentType": file.content_type, "ACL": "public-read"},
    )
    file_url = f'https://{get_s3_creds()[3]}/{S3_MEDIA_BUCKET}/{unique_filename}'
    return file_url

def get_file_s3() -> str:
    get_object_response = s3_client.get_object(Bucket=S3_MEDIA_BUCKET,Key='py_script.py')
