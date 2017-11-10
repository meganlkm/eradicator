from aws_decorators import boto_client
from botocore.exceptions import ClientError

from eradicator.settings import LOGGER


@boto_client('s3')
def __s3_delete_objects(bucket_name, keys, region=None, client=None):
    return client.delete_objects(
        Bucket=bucket_name,
        Delete={
            'Objects': keys
        }
    )


@boto_client('s3', client_type='resource')
def s3_bucket_objects(bucket_name, prefix=None, region=None, client=None):
    try:
        bucket = client.Bucket(bucket_name)
        objects = []
        if prefix:
            objects = bucket.objects.filter(Prefix=prefix)
        else:
            objects = bucket.objects.all()

        keys = [{'Key': obj.key} for obj in objects]
        LOGGER.info({'keys': keys})

        response = __s3_delete_objects(bucket_name, keys, region=region)
        LOGGER.info(response)
    except ClientError as e:
        if "NoSuchBucket" in e.message:
            return {}
        LOGGER.error(repr(e))
        raise e


@boto_client('s3')
def s3_bucket(bucket_name, force=False, region=None, client=None):
    # make sure bucket is empty
    if force:
        s3_bucket_objects(bucket_name, region=region)

    try:
        response = client.delete_bucket(Bucket=bucket_name)
        LOGGER.info(response)
    except ClientError as e:
        if "NoSuchBucket" in e.message:
            return None
        LOGGER.error(repr(e))
        raise e
