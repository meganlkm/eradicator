import ast
import os
import re
from pip.req import parse_requirements
from pip.download import PipSession
from setuptools import setup, find_packages

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

INSTALL_REQS = parse_requirements('requirements.pip', session=PipSession())

_version_re = re.compile(r'__version__\s+=\s+(.*)')
with open('eradicator/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(
        _version_re.search(f.read().decode('utf-8')).group(1)
    ))

setup(
    name='eradicator',
    version=version,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    description='eradicate things',
    long_description='eradicate things',
    url='https://github.com/meganlkm/eradicator',
    author='meganlkm',
    author_email='devstuff.io@gmail.com',
    install_requires=[str(ir.req) for ir in INSTALL_REQS],
    # entry_points={
    #     'console_scripts': [
    #         'eradicate=eradicator:main'
    #     ]
    # }
)
