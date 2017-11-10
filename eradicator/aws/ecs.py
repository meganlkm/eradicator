from aws_decorators import boto_client

from eradicator.settings import LOGGER


def __get_tasks(cluster_name, client):
    paginator = client.get_paginator('list_tasks')
    response_iterator = paginator.paginate(
        cluster=cluster_name
    )
    tasks = []
    for thing in response_iterator:
        tasks.extend(thing['taskArns'])
    return tasks
    # response_iterator = paginator.paginate(
    #     cluster='string',
    #     containerInstance='string',
    #     family='string',
    #     startedBy='string',
    #     serviceName='string',
    #     desiredStatus='RUNNING'|'PENDING'|'STOPPED',
    #     PaginationConfig={
    #         'MaxItems': 123,
    #         'PageSize': 123,
    #         'StartingToken': 'string'
    #     }
    # )


@boto_client('ecs')
def kill_tasks(cluster_name, reason=None, region=None, client=None):
    tasks = __get_tasks(cluster_name, client)
    LOGGER.info(tasks)

    kwargs = {'cluster': cluster_name}
    if reason:
        kwargs['reason'] = reason

    for task in tasks:
        response = client.stop_task(task=task, **kwargs)
        LOGGER.info(response)


@boto_client('ecs')
def cluster(cluster_name, region=None, client=None):
    kill_tasks(cluster_name, 'deleting cluster: {}'.format(cluster_name), region=region)

    # response = client.deregister_container_instance(
    #     cluster='string',
    #     containerInstance='string',
    #     force=True|False
    # )

    # response = client.delete_cluster(
    #     cluster='string'
    # )
