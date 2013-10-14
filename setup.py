#!/usr/bin/env python
# encoding: utf-8

from distutils.core import setup


setup(name='soupy',
    version='0.2.0',
    license='GPLv2',
    description='description',
    author='peterr',
    url='https://github.com/coderiot/soupy/',
    install_requires=['lxml >= 3.0',
                      'cssselect >= 0.8',
                      'requests >= 1.2.3'],
    packages=['soupy']
)
