from setuptools import setup, find_packages

setup(
    name="atelie",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'flask',
        'flask_sqlalchemy',
        'flask_login',
        'flask_migrate'
    ],
)