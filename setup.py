from setuptools import setup
from ascii_art_app.version import __version__

setup(
    name="ASCII_ART_GENERATOR",
    version=__version__,
    long_description=__doc__,
    packages=[
        "ascii_art_app",
        "ascii_art_app.core",
    ],
    install_requires=[
        "numpy==1.19.4", 
        "opencv-python-headless==" # TODO package version number + test
    ],
    extras_require={
        "dev": [
            "pre-commit==2.15.0",
            "pytest==6.2.5",
            "pytest-cov==3.0.0",
            "pytest-env==0.6.2",
            "black==19.3b0",
            "flake8==3.7.8",
            "coverage==6.1.1",
        ]
    },
    entry_points={
        "console_scripts": ["ascii_art_generator = ascii_art_app.main:main"],
    },
)
