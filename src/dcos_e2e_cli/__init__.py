"""
Top level CLI commands.
"""

from .dcos_docker import dcos_docker
from .minidcos import minidcos

__all__ = [
    'dcos_docker',
    'minidcos',
]
