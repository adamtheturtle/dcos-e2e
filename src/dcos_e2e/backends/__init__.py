"""
Classes to allow backend-specific configuration for cluster backend types.
"""

from ._docker import Docker
from ._vagrant import Vagrant

__all__ = [
    "Docker",
    "Vagrant",
]
