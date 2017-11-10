def paginate_filter(paginator, key, params, client):
    paginator = client.get_paginator(paginator)
    response_iterator = paginator.paginate(**params)
    things = []
    for thing in response_iterator:
        things.extend(thing[key])
    return things
