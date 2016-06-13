import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-elegant-choices',
    version='0.1',
    description='An utility for defining enumerations that can be used as choices in Django models',
    long_description=README,
    author='IIIT',
    author_email='contact@iiit.pl',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'six',
        'unittest2',
    ],
    test_suite='runtests.get_suite',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
    ],
)
