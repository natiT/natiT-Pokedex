from setuptools import setup, find_packages

setup(
   name='natiTs_Twitch_Pokedex',
   version='1.0',
   description='Pokedex Command for Twitch',
   author='natiT',
   author_email='-',
   packages= find_packages(),  #same as name
   install_requires=['pandas', 'urllib3', 'fastapi',"cachetools", "uvicorn"], #external packages as dependencies
)