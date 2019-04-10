"""
Create binaries for the CLIs.
"""

import logging
from pathlib import Path
from typing import Set

import docker
from docker.types import Mount

LOGGER = logging.getLogger(__name__)


def make_linux_binaries(repo_root: Path) -> Set[Path]:
    """
    Create binaries for Linux in a Docker container.

    Args:
        repo_root: The path to the root of the repository.

    Returns:
        A set of paths to the built binaries.
    """
    client = docker.from_env(version='auto')

    target_dir = '/e2e'
    code_mount = Mount(
        source=str(repo_root.absolute()),
        target=target_dir,
        type='bind',
    )

    cmd_in_container = [
        # 'pip3',
        # 'install',
        # # See https://github.com/pypa/pip/issues/6163 for why we use this
        # # option.
        # '--no-use-pep517',
        # '.[packaging]',
        # '&&',
        # We override the PyInstaller version installed.
        # This is so that we can get a fix which should be 
        'pip3',
        'install',
        'git+https://github.com/pyinstaller/pyinstaller',
        '&&',
        'pip install .',
        '&&',
        'pip install git+https://github.com/manrajgrover/py-log-symbols',
        '&&',
        'pip uninstall --yes enum34',
	'&&',
        'python',
        'admin/create_pyinstaller_binaries.py',
    ]
    cmd = 'bash -c "{cmd}"'.format(cmd=' '.join(cmd_in_container))

    container = client.containers.run(
        image='python:3.7',
        mounts=[code_mount],
        command=cmd,
        working_dir=target_dir,
        remove=True,
        detach=True,
    )
    for line in container.logs(stream=True):
        line = line.strip()
        LOGGER.info(line)

    dist_dir = repo_root / 'dist'
    return set(dist_dir.iterdir())
