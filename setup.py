from pathlib import Path

import setuptools

VERSION = "1.5"

NAME = "capablanca"

INSTALL_REQUIRES = [
    "numpy>=2.2.1",
    "scipy>=1.15.0",
    "networkx[default]>=3.4.2"
]

setuptools.setup(
    name=NAME,
    version=VERSION,
    description="Approximating the Minimum Vertex Cover within a factor of less than sqrt(2) for an undirected graph represented by a Boolean adjacency matrix in a file.",
    url="https://github.com/frankvegadelgado/capablanca",
    project_urls={
        "Source Code": "https://github.com/frankvegadelgado/capablanca",
        "Documentation Research": "https://www.researchgate.net/publication/388382740_The_Minimum_Vertex_Cover_Problem",
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
            'cover = capablanca.app:main',
            'test_cover = capablanca.test:main'
        ]
    }
)