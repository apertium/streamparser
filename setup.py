from distutils.core import setup
import streamparser

setup(
    name='streamparser',
    version=streamparser.__version__,
    license='GPLv3+',
    description='Python library to parse Apertium stream format',
    keywords='apertium apertium-tools parsing linguistics',
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
    py_modules=['streamparser'],
)
