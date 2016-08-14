# -*- coding: utf-8 -*-
from __future__ import (
    division, absolute_import, print_function, unicode_literals,
)
from builtins import *                  # noqa
from future.builtins.disabled import *  # noqa

from tempfile import NamedTemporaryFile
import random
import string
import base64

import pytest

from img2url.config import load_and_check_config
from img2url.github import load_file, create_file, update_file, list_repo


def random_str(n):
    return ''.join(
        random.SystemRandom().choice(string.ascii_uppercase)
        for _ in range(n)
    )


def tmpfile(content, _disable_gc=[]):
    f = NamedTemporaryFile()
    _disable_gc.append(f)
    with open(f.name, 'w', encoding='utf-8') as _f:
        _f.write(content)
    return f.name


def token():
    _b64token = 'OTBkZGE1MGQyZjBjNTViMGFhYzIwMzE1YmEwYjU2ZmZhMGEyMWY4Mw=='
    t = base64.b64decode(_b64token)
    return t.decode('ascii')


CONFIG_PATH = tmpfile('''
token: {0}
user: img2url-testing
repo: img2url-testing-travisci
'''.format(token()))


def test_config():
    load_and_check_config(CONFIG_PATH)

    bad_path = tmpfile('''
user: img2url-testing
repo: img2url-testing-travisci
''')
    with pytest.raises(RuntimeError):
        load_and_check_config(bad_path)


def test_create_and_update():
    config = load_and_check_config(CONFIG_PATH)

    path = tmpfile(random_str(10))
    assert create_file(path, config).status_code == 201

    _, _, sha = load_file(path)
    assert update_file(path, config, pre_sha=sha).status_code == 201


def test_branch():
    CONFIG_PATH_WITH_BRANCH = tmpfile('''
token: {0}
user: img2url-testing
repo: img2url-testing-travisci
branch: branch-test
'''.format(token()))

    config = load_and_check_config(CONFIG_PATH_WITH_BRANCH)
    path = tmpfile(random_str(10))
    assert create_file(path, config).status_code == 201


def test_path():
    CONFIG_PATH_WITH_PATH = tmpfile('''
token: {0}
user: img2url-testing
repo: img2url-testing-travisci
path: this-is/random-nested-path-{1}/
'''.format(token(), random_str(10)))

    config = load_and_check_config(CONFIG_PATH_WITH_PATH)

    # list an non-existed dir.
    list_repo(config)

    path = tmpfile(random_str(10))
    assert create_file(path, config).status_code == 201
