from eradicator.aws.s3 import bucket, bucket_objects


def s3_bucket_objects(bucket_name, prefix=None, region=None):
    bucket_objects(bucket_name, prefix, region=region)


def s3_bucket(bucket_name, force=False, region=None):
    bucket(bucket_name, force=force, region=region)
