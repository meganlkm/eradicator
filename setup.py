import os
from pip.req import parse_requirements
from pip.download import PipSession
from setuptools import setup, find_packages

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

VERSION = open('VERSION').read().strip()
INSTALL_REQS = parse_requirements('requirements.pip', session=PipSession())

setup(
    name='eradicator',
    version=VERSION,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    description='clean up aws things',
    long_description='clean up aws things',
    url='https://github.com/meganlkm/eradicator',
    author='meganlkm',
    author_email='devstuff.io@gmail.com',
    install_requires=[str(ir.req) for ir in INSTALL_REQS],
    entry_points={
        'console_scripts': [
            'eradicate=eradicator:main'
        ]
    }
)
