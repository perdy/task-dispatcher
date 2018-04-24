# -*- coding: utf-8 -*-

import os
import sys

from setuptools import setup

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

if sys.version_info[0] == 2:
    from codecs import open


def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]


def get_package_data(package):
    """
    Return all files under the root package, that are not in a
    package themselves.
    """
    walk = [(dirpath.replace(package + os.sep, '', 1), filenames)
            for dirpath, dirnames, filenames in os.walk(package)
            if not os.path.exists(os.path.join(dirpath, '__init__.py'))]

    filepaths = []
    for base, filenames in walk:
        filepaths.extend([os.path.join(base, filename)
                          for filename in filenames])
    return {package: filepaths}


# Read requirements
_requirements_file = os.path.join(BASE_DIR, 'requirements.txt')
_tests_requirements_file = os.path.join(BASE_DIR, 'requirements-tests.txt')

# Read description
with open(os.path.join(BASE_DIR, 'README.rst'), encoding='utf-8') as f:
    _LONG_DESCRIPTION = f.read()

_CLASSIFIERS = (
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Natural Language :: English',
    'Programming Language :: Python',
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
    'producer',
    'consumer',
    'scheduler',
])

package_name = 'task_dispatcher'
setup(
    name='task-dispatcher',
    version='1.4.5',
    description='Library that provides a system to generate tasks producers and consumers with ease.',
    long_description=_LONG_DESCRIPTION,
    author='José Antonio Perdiguero López',
    author_email='perdy.hh@gmail.com',
    maintainer='José Antonio Perdiguero López',
    maintainer_email='perdy.hh@gmail.com',
    url='https://github.com/PeRDy/task-dispatcher',
    download_url='https://github.com/PeRDy/task-dispatcher',
    packages=get_packages(package_name),
    packages_data=get_package_data(package_name),
    include_package_data=True,
    install_requires=[
        "Celery",
        "clinner",
        "pyyaml",
        "flower",
    ],
    tests_require=[
        "coverage",
        "nose",
        "prospector",
        "pylint<1.7",
        "sphinx",
        "sphinx_rtd_theme",
        "tox",
    ],
    license='GPLv3',
    zip_safe=False,
    keywords=_KEYWORDS,
    classifiers=_CLASSIFIERS,
    entry_points={
        'console_scripts': [
            'task_dispatcher = task_dispatcher.__main__:main',
        ],
    },
)
