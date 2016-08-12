# -*- coding: utf-8 -*-
from __future__ import (
    division, absolute_import, print_function, unicode_literals,
)
from builtins import *                  # noqa
from future.builtins.disabled import *  # noqa

import os
import os.path

import yaml

from img2url.metadata import AUTHORS, EMAILS


ENV_CONFIG_PATH = 'IMG2URL_CONFIG_PATH'
DEFAULT_CONFIG_PATH = '~/.img2url.conf'


CONFIG_TOKEN = 'token'
CONFIG_USER = 'user'
CONFIG_REPO = 'repo'

# supported parameter.
# * filename
# * sha
# * time
CONFIG_MESSAGE_TEMPLATE_CREATE = 'message_template_create'
CONFIG_MESSAGE_TEMPLATE_UPDATE = 'message_template_update'

CONFIG_COMMITTER_NAME = 'commiter_name'
CONFIG_COMMITTER_EMAIL = 'commiter_email'


DEFAULT_CONFIG = {
    # required.
    CONFIG_TOKEN: None,
    CONFIG_USER: None,
    CONFIG_REPO: None,
    # optional.
    CONFIG_MESSAGE_TEMPLATE_CREATE: '{filename} created by img2url at {time}.',
    CONFIG_MESSAGE_TEMPLATE_UPDATE: '{filename} updated by img2url at {time}.',
    CONFIG_COMMITTER_NAME: AUTHORS[0],
    CONFIG_COMMITTER_EMAIL: EMAILS[0],
}


def locate_config():
    config_path = os.environ.get(ENV_CONFIG_PATH, DEFAULT_CONFIG_PATH)

    if os.path.isfile(config_path):
        return config_path
    else:
        raise RuntimeError(
            'Invalid Config Path: ' + config_path
        )


def load_and_check_config(config_path):

    with open(config_path, encoding='utf-8') as fin:
        user_config = yaml.load(fin)

    missing = []
    config = {}
    for key, value in user_config.items():
        if key not in DEFAULT_CONFIG:
            continue

        value = value or DEFAULT_CONFIG[key]
        if not value:
            missing.append(key)
        config[key] = value

    if missing:
        message = '\n'.join(
            'FATAL: {0} is not defined!'.format(key) for key in missing
        )
        raise RuntimeError(message)

    return config
