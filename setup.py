from importlib.metadata import entry_points
from setuptools import setup
from setuptools import find_packages

setup(
    name='natitdex',
    version='1.0.0',
    description='Python Module for Twitch Command API. Leverage data from pokeapi.com',
    author='natiT',
    author_email='info@natit.de',
    url='github.com',
    packages=find_packages(exclude=('test*')),
    entry_points={
        'console_scripts': [
            'natidex = natitdex.main:main'
        ]
    }

)