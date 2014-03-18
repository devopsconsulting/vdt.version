repo-version-inc
================

This tool will automatically increment the version in a repo.

Each succesful build will create a tag.
A package can be built from a tag.

::

    usage: version [-h] [-p] [-m] [-M] [-b] [-B BUILD_NUMBER] [-c CHANGELOG]
                       [-n] [--plugin PLUGIN] [--skip-build] [--skip-tag] [-v]

    Version increment tool for GIT repositories

    optional arguments:
      -h, --help            show this help message and exit
      -p, --patch           increment the patch number
      -m, --minor           increment minor number
      -M, --major           increment major number
      -b, --build           increment build number
      -B BUILD_NUMBER, --build-number BUILD_NUMBER
                            create a tag with this exact build number
      -c CHANGELOG, --changelog CHANGELOG
                            description of the changes in the new version
      -n, --dry-run         don't perform any changes
      --plugin PLUGIN       The plugin used to get the version and build the
                            package
      --skip-build          tag only, don't build
      --skip-tag            build only, don't tag
      -v, --verbose         more output

Jenkins
=======

This tool is to be used in a jenkins build to automate versioning and packaging.

Automated versioning
--------------------

The default plugin implements versions according to http://semver.org/. It is highly
recommended to use that versioning scheme as well.

Versions are stored as tags in the repository. Each succesful build can yield a new tag.
Each commit will only be tagged *once*. Since we might not need a package from every build,
the tagging of a succesful build and the building of a package can be decoupled
(``--skip-build``, ``--skip-tag``). An example of a vdt-version command that tags a
succesful build is::

    # tag foo
    cd $WORKSPACE/src/foo
    $WORKSPACE/bin/version -v --build-number=$1 --plugin=debianize --skip-build
    git push --tags

Automated packaging
-------------------

Only at the point where we need the packages, they will be
created. For now, the tags are created in the *DEVELOPMENT* environment, and the
packages are built in the *TEST* environment. Packages are built simply by looking up the
latest tag and creating a package from that. An example of a vdt-version command that
builds a package is::

    # build foo package and upload needed files
    cd $WORKSPACE/src/foo
    fakeroot $WORKSPACE/bin/version -v --plugin=debianize --skip-tag
    upload python-foo_*.deb
    upload python-foo.d*.deb
    upload python-puka_*.deb

Here you can see that dependencies are also built automatically (and uploaded to the apt repo).

Plugins
=======

With plugins the version tool can be taught how to version or package your repositories.

Create a new python package in the vdt.versionplugin namespace and implement any of the following methods::

    def get_version() (must return am vdt.versionplugin.shared.Version object)
    def set_version(version) (must return am vdt.versionplugin.shared.Version object)
    def build_package(version)
    def set_package_version(version)

Implementing these methods is **optional**. The ones you don't implement will be taken
from https://github.com/devopsconsulting/vdt.versionplugin.default (WIP)

A good example of a plugin that has packaging covered is: https://github.com/devopsconsulting/vdt.versionplugin.debianize

If your plugin is called ``balla`` it should live in a package called ``vdt.versionplugin.balla``.

The above four methods, if implemented will be imported like this::

    from vdt.versionplugin.balla imported get_version

Extra arguments
===============

When writing a plugin, it might be useful to have some extra arguments, which are passed to your plugin.
Rest assured, that is possible. Any argument unknown to vdt.version will be available in the ``Version``
object passed to ``set_version``, ``build_package`` and ``set_package_version``.

That means in your plugin you can do something like::

    import argparse
    plugin_arg_parser = argparse.ArgumentParser(description="Weeping plugin")
    plugin_arg_parser.p.add_argument("-Q", "--qq", help="Makes the plugin cry")

    def build_package(version):
        plugin_args = plugin_arg_parser.parse_args(version.extra_args)
        # do something and have args parsed!
