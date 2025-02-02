#!/usr/bin/env python3
from setuptools import setup

with open("README.md", "r") as fp:
    long_description = fp.read()


def parse_requirements(filename):
    line_iter = (line.strip() for line in open(filename))
    return [line for line in line_iter if line and not line.startswith("#")]


setup(
    name="fattura",
    version="0.1.0",
    description="parse and generate Italian Fattura Elettronica",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Enrico Zini",
    author_email="emanuele@aecs4u.com",
    url="https://github.com/EmanueleCannizzaro/fattura/",
    license="https://www.apache.org/licenses/LICENSE-2.0.html",
    packages=["fattura"],
    scripts=[
        #"fattura/fattura.py"
    ],
    install_requires=parse_requirements("requirements-lib.txt"),
    test_requires=parse_requirements("requirements-lib.txt"),
    extras_require={
        "formatted_python": ["yapf"],
        "html": ["lxml"],
        "cacerts": ["requests"],
    },
)
