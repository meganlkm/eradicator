from aws_decorators import boto_client

from eradicator.aws import paginate_filter
from eradicator.settings import LOGGER


def __obj_pager(function_name, client_fn, list_name, key,
                all_things=list(), next_marker=None,
                pop_value=None, marker_key_response='NextMarker', marker_key_request='Marker'):
    kwargs = {'FunctionName': function_name}
    if next_marker:
        kwargs[marker_key_request] = next_marker

    try:
        page = client_fn(**kwargs)
        # use jmespath
        all_things.extend([obj[key] for obj in page[list_name]])

        if page.get(marker_key_response):
            __obj_pager(
                function_name=function_name,
                client_fn=client_fn,
                list_name=list_name,
                key=key,
                all_things=all_things,
                next_marker=page[marker_key_response],
                pop_value=pop_value,
                marker_key_response=marker_key_response, marker_key_request=marker_key_request
            )
    except Exception as e:
        if 'ResourceNotFoundException' in repr(e):
            return []
        raise e

    if pop_value:
        try:
            all_things.pop(all_things.index(pop_value))
        except:
            pass

    return all_things


@boto_client('lambda')
def function(function_name, qualifier=None, region=None, client=None):
    kwargs = {'FunctionName': function_name}
    if qualifier:
        kwargs['Qualifier'] = qualifier
    # response = client.delete_function(**kwargs)
    # LOGGER.info({'delete_function': response})
    # try:
    #     client.delete_function(**kwargs)
    # except Exception:
    #     raise


@boto_client('lambda')
def versions(function_name, region=None, client=None):
    fn_versions = __obj_pager(
        function_name=function_name,
        client_fn=client.list_versions_by_function,
        list_name='Versions',
        key='Version',
        pop_value='$LATEST'
    )
    LOGGER.debug({'versions': fn_versions})
    for version in fn_versions:
        function(function_name, qualifier=version, region=region)


@boto_client('lambda')
def aliases(function_name, region=None, client=None):
    fn_aliases = __obj_pager(
        function_name=function_name,
        client_fn=client.list_aliases,
        list_name='Aliases',
        key='Name'
    )
    LOGGER.debug({'aliases': fn_aliases})
    # for alias_name in fn_aliases:
    #     client.delete_alias(FunctionName=function_name, Name=alias_name)


def eradicate(function_name, region=None):
    # event_source_mappings
    # policies
    aliases(function_name, region=region)
    versions(function_name, region=region)
    function(function_name, region=region)
    # log_group
