from setuptools import setup, find_packages

setup(
    name="statsapi",
    version="0.1",
    description="CLI tool for downloading data from MLB's StatsAPI.",
    author="Sam Drapeau",
    author_email="draped4@gmail.com",
    keywords="mlb statsapi cli pitchfx sabermetrics",
    packages=find_packages(exclude=["tests"]),
    install_requires=[
        "Click==7.0",
        "requests==2.23.0"
    ],
    entry_points={"console_scripts": ["statsapi=src.main:cli"]},
)
