# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

import versioneer

with open('README.md', encoding="utf8") as f:
    readme = f.read()

with open('HISTORY.md', encoding="utf8") as f:
    history = f.read()

with open('requirements.txt', encoding="utf8") as f:
    requirements = f.read().split("\n")

setup(
    name="WG",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="zza tool kit ",
    long_description=readme + '\n\n' + history,
    author="Angus",
    author_email="74071365@qq.com",
    keywords="wg",
    url="https://github.com/AngusWG",
    include_package_data=True,
    packages=find_packages(include=["wg", "wg.*"]),
    install_requires=requirements,
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "wg = wg.__main__:main",
            "WG = wg.__main__:main"
        ]
    },
)
