import os

from spylogger import get_logger as get_spylogger

LOGGER = get_spylogger()

BASEDIR = os.path.dirname(os.path.abspath(__file__))

AWS_DEFAULT_REGION = os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
AWS_REGION = os.getenv('AWS_REGION', AWS_DEFAULT_REGION)
