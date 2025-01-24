from pathlib import Path

import setuptools

VERSION = "1.5"

NAME = "capablanca"

INSTALL_REQUIRES = [
    "networkx[default]>=3.4.2",  
    "z3-solver>=4.13.4.0",
    "PuLP>=2.9.0"
]

setuptools.setup(
    name=NAME,
    version=VERSION,
    description="Solve the Boolean Satisfiability (SAT) problem using a DIMACS file as input.",
    url="https://github.com/frankvegadelgado/capablanca",
    project_urls={
        "Source Code": "https://github.com/frankvegadelgado/capablanca",
        "Documentation Research": "https://www.preprints.org/manuscript/202409.2053/v17",
    },
    author="Frank Vega",
    author_email="vega.frank@gmail.com",
    license="MIT License",
    classifiers=[
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
    ],
    python_requires=">=3.10",
    # Requirements
    install_requires=INSTALL_REQUIRES,
    packages=["capablanca"],
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    entry_points={
        'console_scripts': [
            'jaque = capablanca.app:main',
            'batch_jaque = capablanca.test:main'
        ]
    }
)