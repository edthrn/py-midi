"""Setup tool for the package Py-midi
Created by Edouard Theron
Febuary 2017
"""

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='py-midi',
    version='1.2.2',
    description='A package for sending and receiving MIDI messages easily.',
    long_description=long_description,
    url='https://github.com/edouardtheron/py-midi',
    author='Edouard Theron',
    author_email='edouard@edtheron.me',
    license='GNU',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='package library midi music digital serial interface',
    packages=find_packages(),
    install_requires=['pyserial'],
)
