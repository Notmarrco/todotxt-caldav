# -*- coding: utf-8 -*-
"""Todo.txt <-> Caldav VTodo
"""
from setuptools import setup, find_packages

from todotxt_caldav import __version__

requires = ["commandopt", "docopt", "vobject", "todotxtio"]

setup(
    name="TodoTxt Caldav Sync",
    version=__version__,
    description="Sync todo.txt files as Caldav's VTodo",
    url="https://github.com/notmarrco/todotxt-caldav",
    install_requires=requires,
    extras_require={
        "dev": ["pytest", "pytest-pep8", "pytest-cov", "testfixtures", "pylint"],
        "docs": ["sphinx", "recommonmark", "sphinx-material"],
    },
    entry_points={"console_scripts": ["todo2caldav = todotxt_caldav.core:main"]},
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
)
