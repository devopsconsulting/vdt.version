repo-version-inc
================

This tool will automatically increment the version in a repo.


With plugins the version tool can be taught how to version or package your repositories.

Create a new python package in the acp.versionplugin namespace and implement any of the following methods:

```
def get_version()
def set_version(version)
def build_package(version)
def set_package_version(version)
```

The ones you don't implement will be taken from https://github.dtc.avira.com/APC/apc.versionplugin.default (WIP)