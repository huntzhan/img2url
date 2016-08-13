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
DEFAULT_CONFIG_PATH = '~/.img2url.yml'


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

# proxies:
#   http: socks5://127.0.0.1:1080
CONFIG_PROXIES = 'proxies'


class _REQUIRED(object):
    pass


DEFAULT_CONFIG = {
    # required.
    CONFIG_TOKEN: _REQUIRED,
    CONFIG_USER: _REQUIRED,
    CONFIG_REPO: _REQUIRED,

    # optional.
    CONFIG_MESSAGE_TEMPLATE_CREATE: '{filename} created by img2url at {time}.',
    CONFIG_MESSAGE_TEMPLATE_UPDATE: '{filename} updated by img2url at {time}.',

    CONFIG_COMMITTER_NAME: AUTHORS[0],
    CONFIG_COMMITTER_EMAIL: EMAILS[0],

    CONFIG_PROXIES: None,
}


def locate_config():
    config_path = os.environ.get(ENV_CONFIG_PATH, DEFAULT_CONFIG_PATH)
    config_path = os.path.expanduser(config_path)

    if os.path.isfile(config_path):
        return config_path
    else:
        raise RuntimeError(
            'Invalid Config Path: ' + config_path
        )


def process_user_config(user_config):

    missing = []
    config = {}

    for key, default_value in DEFAULT_CONFIG.items():

        value = user_config.get(key, None) or default_value
        if value is _REQUIRED:
            missing.append(key)

        config[key] = value

    if missing:
        message = '\n'.join(
            'FATAL: {0} is not defined!'.format(key) for key in missing
        )
        raise RuntimeError(message)

    return config


def load_and_check_config(config_path):

    with open(config_path, encoding='utf-8') as fin:
        user_config = yaml.load(fin)

    return process_user_config(user_config)
