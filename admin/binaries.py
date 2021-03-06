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

    dist_dir = repo_root / 'dist'
    for path in list(repo_root.glob('dcos-*.spec')) + [dist_dir]:
        container_path = Path(target_dir) / str(path.relative_to(repo_root))
        container = client.containers.run(
            image='python:3.6',
            mounts=[code_mount],
            command=['rm', '-rf', str(container_path)],
            working_dir=target_dir,
            remove=True,
            detach=True,
        )
        for line in container.logs(stream=True):
            line = line.decode().strip()
            LOGGER.info(line)

    bin_dir = repo_root / 'bin'
    binaries = list(bin_dir.iterdir())

    cmd_in_container = ['pip3', 'install', '-e', '.[packaging]']
    for binary in binaries:
        cmd_in_container += [
            '&&',
            'pyinstaller',
            './bin/{binary}'.format(binary=binary.name),
            '--onefile',
        ]
    cmd = 'bash -c "{cmd}"'.format(cmd=' '.join(cmd_in_container))

    container = client.containers.run(
        image='python:3.6',
        mounts=[code_mount],
        command=cmd,
        working_dir=target_dir,
        remove=True,
        detach=True,
    )
    for line in container.logs(stream=True):
        line = line.decode().strip()
        LOGGER.info(line)

    return set(repo_root / 'dist' / binary.name for binary in binaries)
