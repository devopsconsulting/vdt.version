import logging
import contextlib
import sys
import tempfile
import shutil
import glob
from os import getcwd, chdir

from straight.plugin import load


logger = logging.getLogger(__name__)

PLUGIN_NAMESPACE = 'vdt.versionplugin'


class UnknownPlugin(Exception):
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


def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".
    """
    valid = {"yes":True,   "y":True,  "ye":True,
             "no":False,     "n":False}
    if default == None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "\
                             "(or 'y' or 'n').\n")


@contextlib.contextmanager
def change_directory(path=None):
    """
    Context manager that changes directory and resets it when existing
    
    >>> with change_directory('/tmp'):
    >>>     pass
    """
    if path is not None:
        try:
            oldpwd = getcwd()
            logger.debug('changing directory from %s to %s' % (oldpwd, path))
            chdir(path)
            yield
        finally:
            chdir(oldpwd)
    else:
        yield


@contextlib.contextmanager
def empty_directory(path=None):
    """
    Context manager that creates a temporary directory, and cleans it up
    when exiting.
    
    >>> with empty_directory():
    >>>     pass
    """
    install_dir = tempfile.mkdtemp(dir=path)
    try:
        yield install_dir
    finally:
        shutil.rmtree(install_dir)
