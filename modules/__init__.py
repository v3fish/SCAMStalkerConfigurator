# modules/__init__.py

VERSION = "2.3"


def short_version(version=None):
    """Format version without trailing .0 parts (e.g. 2.3.0 -> 2.3)."""
    if version is None:
        version = VERSION
    parts = version.split('.')
    while len(parts) > 1 and parts[-1] == '0':
        parts.pop()
    return '.'.join(parts)
