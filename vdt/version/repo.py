import logging

from vdt.version.utils import load_plugin_by_name


log = logging.getLogger('vdt.version.repo')



class GitRepository(object):
    """
    This class represent a git repository in which tags need
    to be updated and from which debian packages can be built.
    """

    def __init__(self, config):
        self.config = config
        self.default_plugin = load_plugin_by_name('default')
        self.picked_plugin = load_plugin_by_name(config.plugin)
        self.version = None

    def call_plugin_function(self, name, *args, **kwargs):
        # fall back on the default plugin if the method does not
        # exist in the picked_plugin.
        function = getattr(self.picked_plugin, name, getattr(self.default_plugin, name))
        return function(*args, **kwargs)

    def get_version(self, version_args):
        "retrieve latest version with the plugin"
        return self.call_plugin_function('get_version', version_args)
        
    def update_version(self, version, step=1):
        "Compute an new version and write it as a tag"

        # update the version based on the flags passed.
        if self.config.patch:
            version.patch += step
        if self.config.minor:
            version.minor += step
        if self.config.major:
            version.major += step
        if self.config.build:
            version.build_number += step
        if self.config.build_number:
            version.build_number = self.config.build_number

        # create a new tag in the repo with the new version.
        if self.config.dry_run:
            log.info('Not updating repo to version {0}, because of --dry-run'.format(version))
        else:
            version = self.call_plugin_function('set_version', version)

        return version

    def build_package(self, version):
        if self.config.dry_run:
            log.info("Not updatting package version to {0}, because of dry-run".format(version))
        else:
            # if needed update the version in the package
            self.call_plugin_function('set_package_version', version)
            # create a package with the new version.
            return self.call_plugin_function('build_package', version)
