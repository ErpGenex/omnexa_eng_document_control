#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name="omnexa_eng_document_control",
    version="1.0.0",
    description="omnexa_eng_document_control application",
    author="ErpGenEx",
    author_email="info@omnexa.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        "frappe>=15.0.0"
    ]
)
