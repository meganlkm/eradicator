# $ eradicator_

## Setup

#### Set up a virtual environment

```bash
[sudo] pip install virtualenv
virtualenv .venv
source .venv/bin/activate
```

#### Install


```bash
pip install --editable .
```


## Eradicators

### `eradicator.aws.cloudformation`

* `stack(stack_name, region='us-east-1')`

### `eradicator.aws.ecr`

* `repository(repo_name, force=False, region='us-east-1')`
* `images(repo_name, image_ids='all', account=None, region='us-east-1')`

### `eradicator.aws.ecs`

* `kill_tasks(cluster_name, reason=None, region='us-east-1')`
* `services(cluster_name, region='us-east-1')`
* `cluster(cluster_name, stack_name=None, region='us-east-1')`

### `eradicator.aws.lambdas`

* `eradicate(function_name, region='us-east-1')`
* `aliases(function_name, region='us-east-1')`
* `versions(function_name, region='us-east-1')`
* `function(function_name, qualifier=None, region='us-east-1')`

### `eradicator.aws.s3`

* `bucket(bucket_name, force=False, region='us-east-1')`
* `bucket_objects(bucket_name, prefix=None, region='us-east-1')`
