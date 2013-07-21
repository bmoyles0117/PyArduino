#!/usr/bin/env python

from setuptools import setup
import os

def generate_data_files(*dirs):
    results = []

    for src_dir in dirs:
        for root,dirs,files in os.walk(src_dir):
            results.append((root, map(lambda f:root + "/" + f, files)))
    return results

setup(
    name='PyArduino',
    version='0.001',
    description='This library is intended to make programming an Arduino easier for \
                younger programmers. By making a python port of the standard Arduino \
                functions, a young programmer is able to avoid types and the complexities \
                of C and jump right in!',
    author='Bryan Moyles',
    author_email='bryan.moyles@teltechcorp.com',
    url='http://www.bryanmoyles.com/',
    packages=['arduino']
)
