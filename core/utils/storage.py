import os

from django_s3_storage.storage import S3Storage

def get_storage():
    if os.environ.get('AWS_STORAGE_BUCKET_NAME'):
        storage = S3Storage(aws_s3_bucket_name=os.environ.get('AWS_STORAGE_BUCKET_NAME'))
    else:
        storage = None
    return storage