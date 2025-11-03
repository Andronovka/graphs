from setuptools import setup, find_packages

setup(
    name="test_pkg",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
        "numpy>=1.20.0"
    ]
)
