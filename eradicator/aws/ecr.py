from aws_decorators import boto_client

from eradicator.aws import paginate_filter
from eradicator.settings import LOGGER


@boto_client('ecr')
def images(repo_name, image_ids='all', account=None, region=None, client=None):
    if image_ids == 'all':
        image_ids = paginate_filter(
            'list_images',
            'imageIds',
            {'repositoryName': repo_name},
            client
        )

    kwargs = {'repositoryName': repo_name, 'imageIds': image_ids}
    if account:
        kwargs['registryId'] = account
    LOGGER.debug({'kwargs': kwargs})

    response = client.batch_delete_image(**kwargs)
    LOGGER.info({'batch_delete_image': response})


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
