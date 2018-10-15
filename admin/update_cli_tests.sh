#!/usr/bin/env bash

# There are CLI tests which check that --help output for various commands is
# as expected.
#
# Expected output is stored in files.

set -ex

mkdir -p tests/test_cli/test_dcos_docker/help_outputs
git rm -f tests/test_cli/test_dcos_docker/help_outputs/*.txt || true
export FIX_CLI_TESTS=1
pytest tests/test_cli/test_dcos_docker/test_cli.py::TestHelp::test_help || true
git add tests/test_cli/test_dcos_docker/help_outputs/*.txt
