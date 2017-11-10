from aws_decorators import boto_client

from eradicator.aws.cloudformation import stack
from eradicator.settings import LOGGER


def __get_container_instances(cluster_name, client):
    paginator = client.get_paginator('list_container_instances')
    response_iterator = paginator.paginate(
        cluster=cluster_name
    )
    instances = []
    for thing in response_iterator:
        instances.extend(thing['containerInstanceArns'])
    return instances


def __get_tasks(cluster_name, client):
    paginator = client.get_paginator('list_tasks')
    response_iterator = paginator.paginate(
        cluster=cluster_name
    )
    tasks = []
    for thing in response_iterator:
        tasks.extend(thing['taskArns'])
    return tasks


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
def cluster(cluster_name, stack_name=None, region=None, client=None):
    kill_tasks(cluster_name, 'deleting cluster: {}'.format(cluster_name), region=region)

    if stack_name:
        stack(stack_name, region=region)
    else:
        instances = __get_container_instances(cluster_name, client)
        LOGGER.info(instances)
        for ci in instances:
            response = client.deregister_container_instance(
                cluster=cluster_name,
                containerInstance=ci
            )
            LOGGER.info(response)

        # response = client.delete_cluster(
        #     cluster='string'
        # )
