# -*- coding: utf-8 -*-
import sys, os

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

install_requires=[
    "TurboGears2 >= 2.3.1",
    "tgext.pluggable",
    "tw2.core",
    "tw2.forms >= 2.2.0.3",
    "sprox >= 0.9.1",
    'itsdangerous'
]

here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, 'README.rst')).read()
except IOError:
    README = ''

setup(
    name='tgapp-resetpassword',
    version='0.1.10',
    description='Pluggable application for TurboGears2 that permits to change user password or reset it when lost, with sqla and ming compatibility',
    long_description=README,
    author='Simone Gasbarroni',
    author_email='simone.gasbarroni@gmail.com',
    url='https://github.com/gasbasd/tgapp-resetpassword',
    license='MIT',
    keywords='turbogears2.application',
    packages=find_packages(exclude=['ez_setup']),
    install_requires=install_requires,
    include_package_data=True,
    package_data={'resetpassword': [
        'i18n/*/LC_MESSAGES/*.mo',
        'templates/*/*',
        'public/*/*'
    ]},
    message_extractors={'resetpassword': [
            ('**.py', 'python', None),
            ('templates/**.html', 'genshi', None),
            ('public/**', 'ignore', None)
    ]},
    entry_points="""
    """,
    zip_safe=False
)
