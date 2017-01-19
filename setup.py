from distutils.core import setup
import streamparser

setup(
    name='streamparser',
    version=streamparser.__version__,
    license='GPLv3+',
    description='Python library to parse Apertium stream format',
    keywords='apertium parsing linguistics',
    author='Sushain Cherivirala',
    author_email='sushain@skc.name',
    url='https://github.com/goavki/streamparser',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Topic :: Text Processing :: Linguistic',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    py_modules=['streamparser']
)
