import os
from setuptools import setup, find_packages

VERSION = '0.0.1'

def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname), 'r') as file:
        return file.read()

requires = [
    'requests>=2.28.1',
    'msal>=1.18.0'
]

setup(
    name='graphappclient',
    version=VERSION,
    packages=find_packages(),
    url='https://github.com/eshifflett/GraphAppClient',
    license='Apache License 2.0',
    author='eshifflett',
    author_email='eshifflett@users.noreply.github.com',
    maintainer='eshifflett',
    maintainer_email='eshifflett@users.noreply.github.com',
    description='A backend client for interacting with the Microsoft Graph API via application permissions',
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    setup_requires=["wheel"],
    install_requires=requires
)