# -*- coding: utf-8 -*-
from __future__ import (
    division, absolute_import, print_function, unicode_literals,
)
from builtins import *                  # noqa
from future.builtins.disabled import *  # noqa

import os
import os.path

import yaml


ENV_CONFIG_PATH = 'IMG2URL_CONFIG_PATH'
DEFAULT_CONFIG_PATH = '~/.img2url.yml'


def locate_config():
    config_path = os.environ.get(ENV_CONFIG_PATH, DEFAULT_CONFIG_PATH)
    config_path = os.path.expanduser(config_path)

    if os.path.isfile(config_path):
        return config_path
    else:
        raise RuntimeError(
            'Invalid Config Path: ' + config_path
        )


def load_config(config_path):

    with open(config_path, encoding='utf-8') as fin:
        return yaml.load(fin)
