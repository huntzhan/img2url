# -*- coding: utf-8 -*-
from __future__ import (
    division, absolute_import, print_function, unicode_literals,
)
from builtins import *                  # noqa
from future.builtins.disabled import *  # noqa

import base64
import hashlib
from os.path import basename
from datetime import datetime

import requests


API_TEMPLATE = 'https://api.github.com{0}'


# return: (filename, base64 encoded, sha)
def load_file(path):
    with open(path, 'rb') as fin:
        data = fin.read()
    return basename(path), base64.b64encode(data), gitsha(data)


def generate_apienv(path, config):
    filename, content, sha = load_file(path)

    apienv = {
        'filename': filename,
        'sha': sha,
        'content': content,
        'time': str(datetime.now()),
    }
    apienv.update(config)
    return apienv


def headers(config):
    return {
        'Authorization': 'token {token}'.format(**config),
        'Content-Type': 'application/json; charset=utf-8',
    }


def proxies(config):
    return config['proxies']


def requests_kwargs(config):
    return {
        'headers': headers(config),
        'proxies': proxies(config),
    }


def gitsha(data):
    m = hashlib.sha1()
    for arg in [b'blob %u\0' % len(data), data]:
        m.update(arg)
    return m.hexdigest()


def assert_status_code(rep, code):
    if rep.status_code != code:
        raise RuntimeError('FATAL on making request')


def _to_binary(body):
    from requests.compat import json as complexjson
    data = complexjson.dumps(body)
    if not isinstance(data, bytes):
        return data.encode('utf-8')
    else:
        return data


# return [(filename, sha), ...]
def list_repo(config):
    # https://developer.github.com/v3/repos/contents/#response-if-content-is-a-directory

    apiurl = API_TEMPLATE.format(
        '/repos/{user}/{repo}/contents/'.format(**config),
    )

    rep = requests.get(apiurl, **requests_kwargs(config))
    assert_status_code(rep, 200)

    files = []
    for element in rep.json():
        if element['type'] != 'file':
            continue
        files.append(
            (element['name'], element['sha']),
        )
    return files


def _prepare_body(apienv, pre_sha):

    message_template = (
        apienv['message_template_create']
        if pre_sha is None else
        apienv['message_template_update']
    )
    body = {
        'content': apienv['content'],
        'message': message_template.format(**apienv),
        'committer': {
            'name': apienv['commiter_name'],
            'email': apienv['commiter_email'],
        },
    }
    if pre_sha:
        body['sha'] = pre_sha

    return body


# if pre_sha is None, create file.
# otherwise, update file.
def create_or_update_file(path, config, pre_sha=None):
    apienv = generate_apienv(path, config)

    apiurl = API_TEMPLATE.format(
        '/repos/{user}/{repo}/contents/{filename}'.format(**apienv),
    )
    body = _prepare_body(apienv, pre_sha)

    rep = requests.put(
        apiurl,
        json=body,
        **requests_kwargs(config)
    )
    return rep


def create_file(path, config):
    return create_or_update_file(path, config, pre_sha=None)


def update_file(path, config, pre_sha):
    return create_or_update_file(path, config, pre_sha)
