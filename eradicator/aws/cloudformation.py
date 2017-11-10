from aws_decorators import boto_client

from eradicator.settings import LOGGER


@boto_client('cloudformation')
def stack(stack_name, region=None, client=None, *args, **kwargs):
    response = client.delete_stack(StackName=stack_name, **kwargs)
    LOGGER.info(response)
