# -*- coding: utf-8 -*-

import os
import sys

from pip.download import PipSession
from pip.req import parse_requirements
from setuptools import setup

import task_dispatcher

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

if sys.version_info[0] == 2:
    from codecs import open


# Read requirements
_requirements_file = os.path.join(BASE_DIR, 'requirements.txt')
_REQUIRES = [str(r.req) for r in parse_requirements(_requirements_file, session=PipSession())]

# Read description
with open(os.path.join(BASE_DIR, 'README.rst'), encoding='utf-8') as f:
    _LONG_DESCRIPTION = f.read()

_CLASSIFIERS = (
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Natural Language :: English',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Software Development :: Object Brokering',
)
_KEYWORDS = ' '.join([
    'python',
    'stream',
    'data',
    'dispatcher',
    'flow',
    'database',
    'cache',
    'celery',
])

setup(
    name='task-dispatcher',
    version=task_dispatcher.__version__,
    description=task_dispatcher.__description__,
    long_description=_LONG_DESCRIPTION,
    author=task_dispatcher.__author__,
    author_email=task_dispatcher.__email__,
    maintainer=task_dispatcher.__author__,
    maintainer_email=task_dispatcher.__email__,
    url=task_dispatcher.__url__,
    download_url=task_dispatcher.__url__,
    packages=[
        'task_dispatcher',
    ],
    include_package_data=True,
    install_requires=_REQUIRES,
    extras_require={
        'dev': [
            'setuptools',
            'pip',
            'wheel',
            'prospector',
            'twine',
            'bumpversion',
            'pre-commit',
        ]
    },
    license=task_dispatcher.__license__,
    zip_safe=False,
    keywords=_KEYWORDS,
    classifiers=_CLASSIFIERS,
)
