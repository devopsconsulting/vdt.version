import logging

log = logging.getLogger('apc.version.repo')

from apc.version.utils import load_plugin_by_name, UnknowPlugin

class GitRepository(object):
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

    def update_version(self, step=1):
        version = self.call_plugin_function('get_version')
        
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

        if config.dry_run:
            log.info('Not updating repo to version {0}, because of --dry-run'.format(version))
        else:
            self.call_plugin_function('set_version', version)

        return version

    def build_package(self, version):
        if config.dry_run:
            log.info("Not updatting package version to {0}, because of dry-run".format(version))
        else:
            call_plugin_function('set_package_version', version)
            call_plugin_function('build_package', version)

    