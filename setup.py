# coding: utf-8
from setuptools import find_packages, setup

pkgname = "apc.gitverstool"

setup(name=pkgname,
      version="0.0.1",
      description="Version Increment Tool for GIT",
      author="Cosmin Luță",
      author_email="cosmin.luta@avira.com",
      maintainer="Cosmin Luță",
      maintainer_email="cosmin.luta@avira.com",
      packages=find_packages(),
      include_package_data=True,
      namespace_packages=['apc'],
      zip_safe=True,
      install_requires=["setuptools"],
      entry_points={
          'console_scripts':[
              'apc-version = apc.version.main:main'
          ]
      },
)
