# -*- coding: utf-8 -*-
import argparse
import logging
import subprocess

from vdt.version.repo import GitRepository
from vdt.version.shared import VersionError
from vdt.version.utils import query_yes_no, UnknownPlugin


logger = logging.getLogger('vdt.version')


def run(config, extra_args):
    version = None
    try:
        repo = GitRepository(config)
        version = repo.get_version(extra_args)

        if not config.skip_tag:
            version = repo.update_version(version)
            # this is a cludge to avoid programmer error.
            # we don't want the extra args to get lost in update_version.
            if not version.extra_args:
                version.extra_args = extra_args

        if not config.skip_build:
            return repo.build_package(version)

    except (VersionError, UnknownPlugin) as e:
        logger.error(e.message)
        # if something went wrong, ask to undo the tagging.
        msg = "An error occurred, do you need me to remove the tag %s?"
        if version and query_yes_no(msg % version, default="no"):
            subprocess.call(['git', 'tag', '--delete', str(version)])

        return 1


def parse_args(args=None):
    # we keep this is a separate method so we can call this from
    # other software (eg vdt.recipe.version)
    p = argparse.ArgumentParser(
        description="Version increment tool for GIT repositories")

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
    args, extra_args = p.parse_known_args(args)
    return args, extra_args


def main():
    args, extra_args = parse_args()
    loglevel = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=loglevel)
    return run(args, extra_args)


if __name__ == "__main__":
    main()
