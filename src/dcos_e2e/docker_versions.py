"""
Supported versions of Docker for DC/OS.

See
https://docs.mesosphere.com/1.10/installing/oss/custom/system-requirements/#docker
"""

from enum import Enum, auto


class DockerVersion(Enum):
    """
    Supported versions of Docker for DC/OS.
    """

    v1_13_1 = auto()
    v1_11_2 = auto()
