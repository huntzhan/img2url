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

from img2url.config import load_config
from img2url.remotes.github import (
    GitHubConfig, GitHubOperation,
)


def random_str(n):
    return ''.join(
        random.SystemRandom().choice(string.ascii_uppercase)
        for _ in range(n)
    )


def tmpfile(content, _disable_gc=[]):
    f = NamedTemporaryFile(prefix='tmp-img2url-' + random_str(10))
    _disable_gc.append(f)
    with open(f.name, 'w', encoding='utf-8') as _f:
        _f.write(content)
    return f.name


def token():
    _b64token = 'OTBkZGE1MGQyZjBjNTViMGFhYzIwMzE1YmEwYjU2ZmZhMGEyMWY4Mw=='
    t = base64.b64decode(_b64token)
    return t.decode('ascii')


CONFIG_PATH = tmpfile('''
github_token: {0}
github_user: img2url-testing
github_repo: img2url-testing-travisci
'''.format(token()))


def test_config():
    GitHubConfig(load_config(CONFIG_PATH))

    bad_path = tmpfile('''
github_user: img2url-testing
github_repo: img2url-testing-travisci
''')
    with pytest.raises(RuntimeError):
        GitHubConfig(load_config(bad_path))


def test_create_and_update():
    path = tmpfile(random_str(10))

    config = GitHubConfig(load_config(CONFIG_PATH))
    operator = GitHubOperation(config, path)

    assert operator.create_file()
    assert operator.update_file(old_fhash=operator.fhash)


def test_branch():
    CONFIG_PATH_WITH_BRANCH = tmpfile('''
github_token: {0}
github_user: img2url-testing
github_repo: img2url-testing-travisci
github_branch: branch-test
'''.format(token()))

    path = tmpfile(random_str(10))

    config = GitHubConfig(load_config(CONFIG_PATH_WITH_BRANCH))
    operator = GitHubOperation(config, path)

    assert operator.create_file()


def test_path():
    CONFIG_PATH_WITH_PATH = tmpfile('''
github_token: {0}
github_user: img2url-testing
github_repo: img2url-testing-travisci
github_path: this-is/random-nested-path-{1}/
'''.format(token(), random_str(10)))

    path = tmpfile(random_str(10))

    config = GitHubConfig(load_config(CONFIG_PATH_WITH_PATH))
    operator = GitHubOperation(config, path)

    # list an non-existed dir.
    assert operator.list_remote()
