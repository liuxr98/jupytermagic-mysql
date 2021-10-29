from setuptools import _install_setup_requires, setup, find_packages
import os

setup(
    name='mysqlmagic',
    version='1.0.0',
    license = 'BSD',
    description = 'IPython-extension: self-defined mysql magic for IPython',
    author = 'xiaorliu',
    author_email = 'xiaorliu@paypal.com',
    # url = '',
    packages = find_packages(),
    install_requires = [
        'ipython',
        'pandas',
        'pymysql',
    ],
    classifiers = [
        "Framework :: IPython",
        "Programming Language :: Python",
    ]
)