# coding: utf-8
from setuptools import find_packages, setup

pkgname = "vdt.version"

setup(name=pkgname,
      version="0.1.5",
      description="Version Increment Tool for GIT",
      author="Lars van de Kerkhof",
      author_email="lars@devopsconsulting.nl",
      maintainer="Lars van de Kerkhof",
      maintainer_email="lars@devopsconsulting.nl",
      packages=find_packages(),
      include_package_data=True,
      namespace_packages=['vdt'],
      zip_safe=True,
      install_requires=[
          "setuptools",
          "straight.plugin>=1.4.0-post-1",
          "vdt.versionplugin.default",
      ],
      entry_points={
          'console_scripts':[
              'version = vdt.version.main:main'
          ]
      },
)
