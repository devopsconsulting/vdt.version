# -*- coding: utf-8 -*-

import logging
import subprocess
import argparse
import os

BUILD_TAG = "-jenkins-"

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('repo-ver')

def get_build_tags_from_version(base_version, build_tag=BUILD_TAG):
    """
    Return all tags that look like "base_version-BUILD_TAG-buildnumber"
    """
    try:
        args = ['git', 'tag', '-l', "{0}{1}*".format(base_version, build_tag)]
        output = subprocess.check_output(args, stderr=None).strip().split("\n")
        return [line for line in output if line]
    except Exception as e:
        log.exception(e)

def create_new_build_tag(ver, build_number, build_tag=BUILD_TAG):
    """
    Create a new tag in the form of "base_version-build_tag-build_number"
    """
    try:
        version = ".".join(map(str, ver))
        args = ["git", "tag", "{0}{1}{2}".format(version, build_tag, build_number)]
        subprocess.check_call(args)
    except Exception as e:
        log.exception(e)

def create_new_version_tag(ver, changelog, build_tag=BUILD_TAG):
    """
    Create a new tag in the form of "base_version-build_tag-build_number"
    """
    try:
        version = ".".join(map(str, ver))
        args = ["git", "tag", "-a", version, "-m", changelog]
        subprocess.check_call(args)
    except Exception as e:
        log.exception(e)

def _get_latest_build_number(tags):
    """
    Return the latest (highest) build number out of tags. It's assumed that all
    tags are of the same version, so that's not checked anymore.
    """
    if not tags:
        return 0

    def _build_number(tag):
        try:
            return int(tag.split("-")[2])
        except:
            log.error("error fetching build number from {0}".format(tag))
            return 0
    return max(_build_number(tag) for tag in tags)


def get_git_version():
    # First try to get the current version using “git describe”.
    try:
        args = ['git', 'describe', '--abbrev=4']
        line = subprocess.check_output(args, stderr=None)
        version = line.strip()
    except Exception as e:
        log.error(e)
        raise StandardError("version not found")

    if not version:
        raise StandardError("Cannot find the version number!")

    if '-' in version:
        version_number, _ = version.split("-", 1)
        return version_number
    else:
        return version


def main():
    p = argparse.ArgumentParser(description="Version increment tool for GIT repositories")

    p.add_argument("-p", "--patch", dest="patch", default=False, action="store_true", help="increment the patch number")
    p.add_argument("-m", "--minor", dest="minor", default=False, action="store_true", help="increment minor number")
    p.add_argument("-M", "--major", dest="major", default=False, action="store_true", help="increment major number")
    p.add_argument("-b", "--build", dest="build", default=False, action="store_true", help="increment build number")
    p.add_argument("-B", "--build-number", dest="buildnumber", help="create a tag with this exact build number")
    p.add_argument("-c", "--changelog", dest="changelog", help="description of the changes in the new version")

    p.add_argument("-n", "--dry-run", dest="dry_run", default=False, help="don't perform any changes")

    args = p.parse_args()

    try:
        ver_str = get_git_version()
        ver = map(int, ver_str.split(".", 3))
        log.debug("latest version is {0}".format(ver))
    except StandardError:
        log.error("cannot find the current version. Please create an adnotated tag x.y.z!")
        return -1

    try:
        tags = get_build_tags_from_version(ver_str)
        log.debug("build tags for version {0}: {1}".format(ver_str, tags))
    except:
        log.error("cannot get tags")
        return -2

    # See what operation needs to be performed
    ver_changed = False
    if args.patch:
        ver[2] += 1
        ver_changed = True

    if args.minor:
        ver[1] += 1
        ver[2] = 0
        ver_changed = True

    if args.major:
        ver[0] += 1
        ver[1] = 0
        ver[2] = 0
        ver_changed = True

    # if we need to do a version increment, see that we have a changelog
    if ver_changed:
        if not args.changelog:
            log.error("you need to specify a changelog when incrementing a version")
            return -3
        if os.path.isfile(args.changelog):
            with open(args.changelog) as f:
                changelog = f.read()
        else:
            changelog = args.changelog

        create_new_version_tag(ver, changelog)

    if args.buildnumber:
        build_number = int(args.buildnumber)
        log.debug("creating build number: {0}".format(build_number))
        create_new_build_tag(ver, build_number)
    elif args.build:
        last_build_number = _get_latest_build_number(tags)
        log.debug("latest build number for version {0}: {1}".format(ver_str, last_build_number))
        last_build_number += 1
        log.debug("incremented build number: {0}".format(last_build_number))
        create_new_build_tag(ver, last_build_number)

if __name__ == "__main__":
    main()

