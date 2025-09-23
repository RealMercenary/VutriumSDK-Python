#!/usr/bin/env python3
"""
VutriumSDK Python Implementation
A pure Python implementation of the VutriumSDK for Rocket League bot development.
"""

from setuptools import setup, find_packages
import os

# Read the contents of README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Read requirements
with open(os.path.join(this_directory, 'requirements.txt'), encoding='utf-8') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    # Filter out built-in modules
    requirements = [req for req in requirements if not req.split('>=')[0].strip() in 
                   ['socket', 'threading', 'time', 'json', 'struct', 'logging']]

setup(
    name="vutriumsdk-python",
    version="1.0.0",
    author="VutriumSDK Team",
    author_email="contact@vutriumsdk.dev",
    description="A pure Python implementation of the VutriumSDK for Rocket League bot development",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/VutriumSDK-Python",
    py_modules=["VutriumSDK"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Games/Entertainment",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: Microsoft :: Windows",
    ],
    keywords="rocket-league bot rlbot gaming vutrium sdk",
    python_requires=">=3.11",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=0.991",
        ],
        "enhanced": [
            "requests>=2.28.0",
            "numpy>=1.21.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "vutrium-demo=example_client:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    project_urls={
        "Bug Reports": "https://github.com/yourusername/VutriumSDK-Python/issues",
        "Source": "https://github.com/yourusername/VutriumSDK-Python",
        "Documentation": "https://github.com/yourusername/VutriumSDK-Python#readme",
    },
)