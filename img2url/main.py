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


# def conditional_upload_file(path, config):
#
#     fname, _, sha = load_file(path)
#
#     # load remote files.
#     exists_files = list_repo(config)
#
#     for remote_fname, remote_sha in exists_files:
#         if sha != remote_sha and fname != remote_fname:
#             continue
#
#         # case 1, file already exists in remote.
#         if sha == remote_sha:
#             return remote_fname
#
#         # case 2, filename conflicts, treat it as update.
#         if fname == remote_fname:
#             rep = update_file(path, config, pre_sha=remote_sha)
#             return extract_filename(rep)
#
#     # case 3, file not exists.
#     rep = create_file(path, config)
#     return extract_filename(rep)


def upload_file(fpath, fields, RemoteConfig, RemoteOperation):

    config = RemoteConfig(fields)
    operator = RemoteOperation(config, fpath)

    ret_fname = None

    # load remote files.
    exists_files = operator.list_repo()

    for remote_fname, remote_fhash in exists_files:

        if operator.fhash != remote_fhash and operator.fname != remote_fname:
            # not this one.
            continue

        if operator.fhash == remote_fhash:
            # case 1, file already exists in remote.
            ret_fname = remote_fname
            break

        if operator.fname == remote_fname:
            # case 2, filename conflicts, treat it as update.
            ret_fname = operator.update_file(old_fhash=remote_fhash)
            break

    # case 3, file not exists.
    ret_fname = operator.create_file()

    # return corresponding url.
    return ret_fname, operator.resource_url(ret_fname)


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
