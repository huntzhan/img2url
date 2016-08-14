# -*- coding: utf-8 -*-
from __future__ import (
    division, absolute_import, print_function, unicode_literals,
)
from builtins import *                  # noqa
from future.builtins.disabled import *  # noqa

from docopt import docopt

from img2url.metadata import VERSION
from img2url.config import locate_config, load_and_check_config
from img2url.github import load_file, list_repo, create_file, update_file


DOC = '''
Usage:
    img2url <path>
    img2url (-m | --markdown) <path>

Options:
    -m, --markdown
'''


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


def conditional_upload_file(path, config):
    fname, _, sha = load_file(path)

    # load remote files.
    exists_files = list_repo(config)

    for remote_fname, remote_sha in exists_files:
        if sha != remote_sha and fname != remote_fname:
            continue

        # case 1, file already exists in remote.
        if sha == remote_sha:
            return remote_fname

        # case 2, filename conflicts, treat it as update.
        if fname == remote_fname:
            update_file(path, config, pre_sha=remote_sha)
            return remote_fname

    # case 3, file not exists.
    create_file(path, config)
    return fname


def download_url(filename, config):
    URL = (
        'https://cdn.rawgit.com/{user}/{repo}/master/{filename}'
    )
    return URL.format(filename=filename, **config)


def entry_point():
    args = docopt(DOC, version=VERSION)

    path = args['<path>']
    doc_type = get_doc_type(args)

    config = load_and_check_config(locate_config())
    filename = conditional_upload_file(path, config)

    url = translate_url(
        filename,
        download_url(filename, config),
        doc_type,
    )
    print(url)
