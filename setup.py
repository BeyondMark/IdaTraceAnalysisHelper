# -*- coding: utf-8 -*-
import setuptools

with open("README.md", "r",encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ida_trace_analysis_helper",
    version="0.0.2",
    author="beyond_mark",
    author_email="luck.yangbo@gmail.com",
    description="parse the ida trace file and track the register from",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BeyondMark/IdaTraceAnalysisHelper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
