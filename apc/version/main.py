# -*- coding: utf-8 -*-
import logging
import argparse
import subprocess

from apc.version.repo import GitRepository
from apc.version.shared import VersionNotFound
from apc.version.utils import UnknownPlugin

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('apc.version')


def main():
    p = argparse.ArgumentParser(description="Version increment tool for GIT repositories")

    p.add_argument("-p", "--patch", default=False, action="store_true", help="increment the patch number")
    p.add_argument("-m", "--minor", default=False, action="store_true", help="increment minor number")
    p.add_argument("-M", "--major", default=False, action="store_true", help="increment major number")
    p.add_argument("-b", "--build", default=False, action="store_true", help="increment build number")
    p.add_argument("-B", "--build-number", dest="build_number", help="create a tag with this exact build number")
    p.add_argument("-c", "--changelog", dest="changelog", help="description of the changes in the new version")
    p.add_argument("-n", "--dry-run", dest="dry_run", default=False, action="store_true", help="don't perform any changes")
    p.add_argument("--plugin", default='default', help='The plugin used to get the version and build the package')

    args = p.parse_args()

    try:
        repo = GitRepository(args)
        new_version = repo.update_version()
        repo.build_package(new_version)
    except (VersionError ,UnknownPlugin) as e:
        logging.error(e.message)
        # if something went wrong undo the tagging.
        subprocess.call(['git', 'tag', '--delete=%s' % new_version])


if __name__ == "__main__":
    main()

