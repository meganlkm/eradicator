from aws_decorators import boto_client

from eradicator.aws.cloudformation import stack
from eradicator.settings import LOGGER


def __get_things(paginator, key, cluster_name, client):
    paginator = client.get_paginator(paginator)
    response_iterator = paginator.paginate(
        cluster=cluster_name
    )
    things = []
    for thing in response_iterator:
        things.extend(thing[key])
    return things


@boto_client('ecs')
def kill_tasks(cluster_name, reason=None, region=None, client=None):
    tasks = __get_things('list_tasks', 'taskArns', cluster_name, client)
    LOGGER.info(tasks)

    kwargs = {'cluster': cluster_name}
    if reason:
        kwargs['reason'] = reason

    for task in tasks:
        response = client.stop_task(task=task, **kwargs)
        LOGGER.info(response)


@boto_client('ecs')
def services(cluster_name, region=None, client=None):
    services = __get_things('list_services', 'serviceArns', cluster_name, client)
    LOGGER.info(services)

    for svc in services:
        kwargs = {'cluster': cluster_name, 'service': svc}
        client.update_service(desiredCount=0, **kwargs)
        response = client.delete_service(**kwargs)
        LOGGER.info(response)


@boto_client('ecs')
def cluster(cluster_name, stack_name=None, region=None, client=None):
    kill_tasks(cluster_name, 'deleting cluster: {}'.format(cluster_name), region=region)

    if stack_name:
        stack(stack_name, region=region)
    else:
        instances = __get_things('list_container_instances', 'containerInstanceArns', cluster_name, client)
        LOGGER.info(instances)
        for ci in instances:
            response = client.deregister_container_instance(
                cluster=cluster_name,
                containerInstance=ci
            )
            LOGGER.info(response)
        # what else....

    services(cluster_name, region=region)
    response = client.delete_cluster(cluster=cluster_name)
    LOGGER.info(response)
