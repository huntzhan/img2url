# -*- coding: utf-8 -*-
from __future__ import (
    division, absolute_import, print_function, unicode_literals,
)
from builtins import *                  # noqa
from future.builtins.disabled import *  # noqa

from docopt import docopt

from img2url.metadata import VERSION

from img2url.config import locate_config, load_config

from img2url.remotes.github import GitHubConfig, GitHubOperation
from img2url.remotes.qiniu import QiniuConfig, QiniuOperation


DOC = '''
Usage:
    img2url <path>
    img2url (-m | --markdown) <path>

Options:
    -m, --markdown
'''

CONFIG_REMOTE = 'remote'

REGISTERED_REMOTES = {
    'github': (GitHubConfig, GitHubOperation),
    'qiniu': (QiniuConfig, QiniuOperation),
}


def translate_url(filename, url, doc_type):
    TEMPLATES = {
        'original': '{url}',
        'markdown': '![{filename}]({url})',
    }
    return TEMPLATES[doc_type].format(filename=filename, url=url)


def get_doc_type(args):
    for doc_type in [
        'markdown',
    ]:
        if args.get('--{0}'.format(doc_type), None):
            return doc_type

    return 'original'


def upload_file(fpath, fields, RemoteConfig, RemoteOperation):

    config = RemoteConfig(fields)
    operator = RemoteOperation(config, fpath)

    ret_fname = None

    # load remote files.
    exists_files = operator.list_remote()

    fname2fhash = {n: h for n, h in exists_files}
    fhash2fname = {h: n for n, h in exists_files}

    if operator.fhash in fhash2fname:
        # case 1, file already exists in remote.
        ret_fname = fhash2fname[operator.fhash]

    elif operator.fname in fname2fhash:
        # case 2, filename conflicts, treat it as update.
        ret_fname = operator.update_file(old_fhash=fname2fhash[operator.fname])

    else:
        # case 3, file not exists.
        ret_fname = operator.create_file()

    # return corresponding url.
    return ret_fname, operator.resource_url(ret_fname, operator.fhash)


def entry_point():
    args = docopt(DOC, version=VERSION)

    path = args['<path>']
    doc_type = get_doc_type(args)

    fields = load_config(locate_config())

    # load operator.
    remote = fields.get(CONFIG_REMOTE, 'github')
    if remote not in REGISTERED_REMOTES:
        raise RuntimeError(
            'FATAL: {0} is not a valid remote type.'.format(remote),
        )
    RemoteConfig, RemoteOperation = REGISTERED_REMOTES[remote]

    ret_fname, resource_url = upload_file(
        path, fields, RemoteConfig, RemoteOperation,
    )

    url = translate_url(
        ret_fname,
        resource_url,
        doc_type,
    )
    print(url)
