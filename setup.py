# -*- coding: utf-8 -*-
"""
    Copyright (C) Quizzingbricks 2013
"""

from setuptools import setup, find_packages

setup(
    name="Quizzingbricks",
    version="0.1-beta",
    author="QuizzingBricks",
    author_email="d7017e@groups.google.com", # or?
    description="Quizzingbricks is a quiz game",
    package_dir={"": "src/python"},
    packages=find_packages("src/python"),
    include_package_data=True,
    zip_safe=False,
    platforms="any",
    install_requires=[
        "flask",
        "sqlalchemy",
        "alembic",
        "psycopg2",
        "gevent",
        "pyzmq",
        "redis",
        "bcrypt",
        "protobuf",
        "gunicorn",
    ]
)