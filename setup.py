#!/usr/bin/env python
# encoding: utf-8

from distutils.core import setup

setup(name='soupy',
    version='0.1.0',
    description='description',
    author='peterrr',
    url='https://github.com/peterrr/soupy/',
    install_requires=['lxml >= 3.0',
                      'cssselect >= 0.8',
                      'mechanize'],
    py_modules=['soupy']
)
