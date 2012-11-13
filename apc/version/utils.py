from straight.plugin import load


PLUGIN_NAMESPACE = 'apc.versionplugin'

class UnknowPlugin(Exception):
    def __init__(self, plugins):
        self.message = "Plugin unknown, try one of %s" % plugins


def load_plugin_by_name(name):
    """
    Load the plugin with the specified name.
    
    >>> plugin = load_plugin_by_name('default')
    >>> api = dir(plugin)
    >>> 'build_package' in api
    True
    >>> 'get_version' in api
    True
    >>> 'set_package_version' in api
    True
    >>> 'set_version' in api
    True
    """
    plugins = load(PLUGIN_NAMESPACE)
    full_name = "%s.%s" % (PLUGIN_NAMESPACE, name)
    try:
        plugin = (plugin for plugin in plugins if plugin.__name__ == full_name).next()
        return plugin
    except StopIteration:
        raise UnknownPlugin([plugin.__name__.split('.').pop() for plugin in plugins])