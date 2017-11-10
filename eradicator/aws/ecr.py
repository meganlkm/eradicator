from aws_decorators import boto_client

from eradicator.settings import LOGGER


@boto_client('ecr')
def repository(repo_name, force=False, region=None, client=None):
    try:
        client.delete_repository(repositoryName=repo_name, force=force)
    except Exception as e:
        msg = repr(e)
        if 'RepositoryNotFoundException' in msg:
            return None
        if 'RepositoryNotEmptyException' in msg:
            LOGGER.error({'help': 'use the force to eradicate this repository'})
        raise e
