#!/usr/bin/env python
import setuptools

setuptools.setup(
    name="gcptool",
    version="0.0.1",
    packages=setuptools.find_packages(),
    author="Aidan Noll",
    author_email="aidan.noll@carvesystems.com",
    entry_points={
        "console_scripts": ["gcptool=gcptool.__main__:main"],
    },
    # scripts = []
    install_requires=[
        "google-cloud-resource-manager",
        "google-cloud-container",
        "google-cloud-storage",
        "google-api-python-client",
        "jinja2",
        "netaddr",
        "pydantic",
    ],
    python_requires=">=3.7",
)
