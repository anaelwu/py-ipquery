#-*- coding:utf-8 -*-
'''
Created on 2018-05-23

@author: ranyixu
'''

from setuptools import setup, find_packages

setup(
    name='ipquery',
    version='0.0.1',
    author='ranyixu',
    author_email='1015243376@qq.com',
    packages=find_packages(),
    include_package_data = True,
    zip_safe = False,
    keywords = ['ip_query', 'ip', 'asyncio'],
    install_requires = ["aiohttp"],
    description='A ip query implemention based on taobao api',
    classifiers=[  
        "Intended Audience :: Developers",  
        "Operating System :: OS Independent",  
        "Topic :: System :: Networking",  
        "Topic :: Software Development :: Libraries :: Python Modules",  
        "Programming Language :: Python :: 3.4",  
        "Programming Language :: Python :: 3.5",  
        "Programming Language :: Python :: 3.6",  
    ]
)
