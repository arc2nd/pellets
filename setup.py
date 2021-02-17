#!/usr/bin/env python

import re
import io
import os

from setuptools import find_packages
from setuptools import setup


def read(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    text_type = type(u"")
    with io.open(filename, mode='r', encoding='utf-8') as fp:
        return re.sub(text_type(r":[a-z]+:'~?(.*)'"), text_type(r"``\1``"), fp.read())

setup(
    name='pellets',
    version='0.1.2', 
    url='192.168.1.85/arc2nd/pellets', 
    license='Proprietary', 

    author='James Parks', 
    author_email='james_parks@hotmail.com', 

    description='a wrapper around RabbitMQ using pika', 
    long_description=read('README.rst'), 

    classifiers=[
        'Developement Status :: 2 - Pre-Alpha', 
        'License :: Other/Proprietary License', 
        'Programming Language :: Python', 
        'Programming Language :: Python :: 3.9', 
    ], 

    packages=find_packages(exclude=('tests', )),

    install_requires=['pika', 'cryptography'], 
    extras_require={
        'dev': ['pytest==5.3.5', 'tox==3.14.3']
    }
)
