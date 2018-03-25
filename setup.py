from os import path
from setuptools import setup

import streamparser

setup(
    name='apertium-streamparser',
    version=streamparser.__version__,
    license=streamparser.__license__,
    description='Python library to parse Apertium stream format',
    long_description=open(path.join(path.abspath(path.dirname(__file__)), 'README.md')).read(),
    long_description_content_type='text/markdown; charset=UTF-8',
    keywords='apertium parsing linguistics',
    author='Sushain K. Cherivirala',
    author_email='sushain@skc.name',
    url='https://github.com/apertium/streamparser',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Topic :: Text Processing :: Linguistic',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    python_requires='>=3.4',
    entry_points={
        'console_scripts': ['apertium-streamparser=streamparser:main'],
    },
    py_modules=['streamparser'],
)
