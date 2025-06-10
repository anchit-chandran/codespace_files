from setuptools import setup, find_packages

setup(
    name="medicode",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "click>=8.1.7",
        "rich>=13.7.0",
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "medicode=medicode_cli.__main__:cli",
        ],
    },
) 