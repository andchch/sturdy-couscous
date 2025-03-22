import json
from uuid import uuid4

import boto3
from fastapi import UploadFile

from backend.api_v1.users.dao import UserDAO
from backend.core.config import get_s3_creds
from backend.redis.cache import RedisController

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
        ExtraArgs={'ContentType': file.content_type, 'ACL': 'public-read'},
    )
    file_url = f'https://{get_s3_creds()[3]}/{bucket}/{unique_filename}'
    return file_url

def get_user_avatar(filename: str) -> str:
    # Generate the S3 presigned URL
    s3_presigned_url = s3_client.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': 'user.media',
            'Key': f'{filename}'
        },
        ExpiresIn=3600 # 1 hour
    )
    return s3_presigned_url

async def get_cached_avatar_url(id: int, redis_controller: RedisController, url: str = None) -> str:
    if url is None:
        user = await UserDAO.get_by_id(id)
        if user.avatar_url is None:
            return 'no avatar'
        if user.avatar_url == 'empty':
            return 'https://raw.githubusercontent.com/saveryanov/avatars/refs/heads/master/examples/username.png'
        else:
            file_key = user.avatar_url.split('/')[-1]
    else:
        if url == 'empty' or url == 'https://raw.githubusercontent.com/saveryanov/avatars/refs/heads/master/examples/username.png':
            return 'https://raw.githubusercontent.com/saveryanov/avatars/refs/heads/master/examples/username.png'
        file_key = url.split('/')[-1]
        
    cache_key = f'presigned_avatar_url:{id}'

    cached_url = await redis_controller.redis.get(cache_key)
    if cached_url:
        return json.loads(cached_url)

    presigned_url = s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': 'user.media',
                'Key': file_key},
        ExpiresIn=60,  # Срок действия URL (15 min)
    )
    
    await redis_controller.redis.set(cache_key, json.dumps(presigned_url), ex=60)
    
    return presigned_url

async def get_cached_media_url(file_url: str, media_id: int, redis_controller: RedisController) -> str:
    file_key = file_url.split('/')[-1]
    cache_key = f'presigned_media_url:{media_id}'

    cached_url = await redis_controller.redis.get(cache_key)
    if cached_url:
        return json.loads(cached_url)

    presigned_url = s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': 'bucket-913415',
                'Key': file_key},
        ExpiresIn=1800,  # Срок действия URL (30 min)
    )
    
    await redis_controller.redis.set(cache_key, json.dumps(presigned_url), ex=1800)
    
    return presigned_url
