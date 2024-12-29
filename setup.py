from pathlib import Path

import setuptools

VERSION = "1.1"

NAME = "capablanca"

INSTALL_REQUIRES = [
    "z3-solver>=4.13.4.0"
]


setuptools.setup(
    name=NAME,
    version=VERSION,
    description="Solve the Boolean Satisfiability (SAT) problem using a DIMACS file as input.",
    url="https://github.com/frankvegadelgado/capablanca",
    project_urls={
        "Source Code": "https://github.com/frankvegadelgado/capablanca",
    },
    author="Frank Vega",
    author_email="vega.frank@gmail.com",
    license="MIT License",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
    ],
    # Snowpark requires Python 3.8
    python_requires=">=3.8",
    # Requirements
    install_requires=INSTALL_REQUIRES,
    packages=["capablanca"],
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    entry_points={
        'console_scripts': [
            'jaque = capablanca.satpy:main'
        ]
    }
)
