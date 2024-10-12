"""
Classes to allow backend-specific configuration for cluster backend types.
"""

from ._docker import Docker

__all__ = [
    'Docker',
]
