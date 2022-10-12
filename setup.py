from setuptools import setup
from setuptools import find_packages

setup(
    name='natitdex',
    version='1.0.0',
    description='Python Module for Twitch Command API. Leverage data from pokeapi.com',
    author='natiT',
    author_email='info@natit.de',
    url='https://github.com/natiT/natiT-Pokedex',
    license='MIT',
    packages=find_packages(exclude=('test*')),
    entry_points={
        'console_scripts': [
            'natidex = natitdex.main:main'
        ]
    },
    install_requires=['pandas', 'urllib3', 'fastapi',"cachetools", "uvicorn","requests","emoji"]
)
