# -*- coding: utf-8 -*-
import logging
import argparse
import subprocess

from vdt.version.repo import GitRepository
from vdt.version.shared import VersionError
from vdt.version.utils import UnknownPlugin

def run(config):
    try:
        repo = GitRepository(config)
        version = repo.get_version()
        if not config.skip_tag:
            version = repo.update_version(version)
        if not config.skip_build:
            repo.build_package(version)
    except (VersionError, UnknownPlugin) as e:
        logging.error(e.message)
        # if something went wrong undo the tagging.
        subprocess.call(['git', 'tag', '--delete=%s' % new_version])


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
    p.add_argument("--skip-build", default=False, dest="skip_build" , action="store_true", help="tag only, don't build")
    p.add_argument("--skip-tag", default=False, dest="skip_tag", action="store_true", help="build only, don't tag")
    p.add_argument("-v", "--verbose", default=False, dest="verbose", action="store_true", help="more output")
    args = p.parse_args()
    
    loglevel = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=loglevel)
    log = logging.getLogger('vdt.version')
    
    run(args)


if __name__ == "__main__":
    main()

