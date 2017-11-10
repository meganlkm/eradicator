from aws_decorators import boto_client
from botocore.exceptions import ClientError

from eradicator.settings import LOGGER


@boto_client('s3')
def __delete_objects(bucket_name, keys, region=None, client=None):
    return client.delete_objects(
        Bucket=bucket_name,
        Delete={
            'Objects': keys
        }
    )


@boto_client('s3', client_type='resource')
def bucket_objects(bucket_name, prefix=None, region=None, client=None):
    objects = []
    try:
        bucket_objects = client.Bucket(bucket_name).objects
        if prefix:
            objects = bucket_objects.filter(Prefix=prefix)
        else:
            objects = bucket_objects.all()
        keys = [{'Key': obj.key} for obj in objects]
        LOGGER.info({'keys': keys})

        response = __delete_objects(bucket_name, keys, region=region)
        LOGGER.info(response)
    except ClientError as e:
        if "NoSuchBucket" not in e.message:
            LOGGER.error(repr(e))
            raise e


@boto_client('s3')
def bucket(bucket_name, force=False, region=None, client=None):
    try:
        # make sure bucket is empty
        if force:
            bucket_objects(bucket_name, region=region)
        response = client.delete_bucket(Bucket=bucket_name)
        LOGGER.info(response)
    except ClientError as e:
        if "NoSuchBucket" not in e.message:
            LOGGER.error(repr(e))
            raise e
