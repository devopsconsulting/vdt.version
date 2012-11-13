BUILD_TAG = 'jenkins'


def parse_version_string(version_string):
    """
    Parse a version string into it's components.
    
    >>> parse_version_string("0.1")
    ([0, 1], None, None)
    >>> parse_version_string("0.3.2-jenkins-3447876")
    ([0, 3, 2], 'jenkins', 3447876)
    """
    components = version_string.split('-') + [None, None]
    version = map(int, components[0].split('.'))
    build_tag = components[1]
    build_number = int(components[2]) if components[2] else components[2]

    return (version, build_tag, build_number)


def format_version(version, build_number=None, build_tag=BUILD_TAG):
    """
    Format a version string for use in packaging.
    
    >>> format_version([0,3,5])
    '0.3.5'
    >>> format_version([8, 8, 9], 23676)
    '8.8.9-jenkins-23676'
    >>> format_version([8, 8, 9], 23676, 'koekjes')
    '8.8.9-koekjes-23676'
    """
    formatted_version = ".".join(map(str, version))

    if build_number is not None:
        return "{formatted_version}-{build_tag}-{build_number}".format(**locals())
    
    return formatted_version


class VersionNotFound(Exception):
    pass


class Version(object):
    """
    Represent a version object with a nice
    interface for incrementing.
    
    >>> a = Version('1.2.3-koe-4646')
    >>> a.patch += 4
    >>> str(a)
    '1.2.7-koe-4646'
    >>> a.minor += 3
    >>> str(a)
    '1.5.0-koe-4646'
    >>> a.major += 3
    >>> str(a)
    '4.0.0-koe-4646'
    >>> a.build_tag = 'lol'
    >>> str(a)
    '4.0.0-lol-4646'
    >>> a.build_number = 876876
    >>> str(a)
    '4.0.0-lol-876876'
    """
    def __init__(self, version_string):
        (version, self.build_tag, self.build_number) = \
            parse_version_string(version_string)
        
        version.extend([0, 0, 0])
        self._major = version[0]
        self._minor = version[1]
        self.patch = version[2]

    @property
    def major(self):
        return self._major

    @major.setter
    def major(self, value):
        self._major = value
        self._minor = 0
        self.patch = 0

    @property
    def minor(self):
        return self._minor

    @minor.setter
    def minor(self, value):
        self._minor = value
        self.patch = 0

    @property
    def version(self):
        return [self._major, self._minor, self.patch]

    def __str__(self):
        if self.build_number is not None:
            return format_version(self.version, self.build_number, self.build_tag)
        return format_version(self.version)

    __unicode__ = __str__
