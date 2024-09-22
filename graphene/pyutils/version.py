from __future__ import unicode_literals
import datetime
import os
import subprocess


def get_version(version=None):
    """Returns a PEP 440-compliant version number from VERSION."""
    pass


def get_main_version(version=None):
    """Returns main version (X.Y[.Z]) from VERSION."""
    pass


def get_complete_version(version=None):
    """Returns a tuple of the graphene version. If version argument is non-empty,
    then checks for correctness of the tuple provided.
    """
    pass


def get_git_changeset():
    """Returns a numeric identifier of the latest git changeset.
    The result is the UTC timestamp of the changeset in YYYYMMDDHHMMSS format.
    This value isn't guaranteed to be unique, but collisions are very unlikely,
    so it's sufficient for generating the development version numbers.
    """
    pass
