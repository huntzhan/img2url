# -*- coding: utf-8 -*-
from __future__ import (
    division, absolute_import, print_function, unicode_literals,
)
from builtins import *                  # noqa
from future.builtins.disabled import *  # noqa

from os.path import basename, splitext, expanduser, exists


# Thie file defines the interfaces that developer *must* override to support
# new remote type, including operations related to configuration,
# authentication and url rendering.


# class as special value.
class REQUIRED_FIELD(object):
    pass


class Configuration(object):

    # subclass should override FIELDS.
    # FIELDS = [
    #     # required field.
    #     ('<key>', REQUIRED_FIELD),
    #     # optional field.
    #     ('<key>', None),
    #     ('<key>', 'brbrbr'),
    # ]
    FIELDS = None

    def __init__(self, fields):
        self._extract_and_validate(fields)
        self.postprocess_fields()

    def _extract_and_validate(self, user_fields):

        self.fields = {}

        missing = []
        # only extract fields defined in FIELDS.
        for key, default in self.FIELDS:

            value = user_fields.get(key, None) or default
            # record missing required fields.
            if value is REQUIRED_FIELD:
                missing.append(key)

            self.fields[key] = value

        if missing:
            message = '\n'.join(
                'FATAL: {0} is not defined!'.format(key) for key in missing
            )
            # TODO(huntzhan): enhance logging.
            raise RuntimeError(message)

    # user could override this method to perform post-processing.
    def postprocess_fields(self):
        pass


class OperationPackage(object):

    def __init__(self, config, fpath):
        self.config = config
        self._setup_file(fpath)
        self.init()

    def get_config(self, key):
        return self.config.fields.get(key, None)

    # fpath: ab
    def _setup_file(self, fpath):
        fpath = expanduser(fpath)
        if not exists(fpath):
            # TODO(huntzhan): enhance logging.
            raise RuntimeError('FATAL: {0} not exists'.format(fpath))

        # fpath:           abspath of file.
        # fname:           filename of file.
        # fbasename:       filename without ext.
        # fext:            ext of file.
        # fdata:           binary data of file.
        # fhash:           hash value of file, defined by user.
        # fname_with_hash: fname + '-' + fhash + fext
        self.fpath = fpath
        self.fname = basename(fpath)
        self.fbasename, self.ext = splitext(self.fname)

        with open(fpath, 'rb') as fin:
            self.fdata = fin.read()
        self.fhash = self.generate_file_hash(self.fdata)

        # mainly for update.
        self.fname_with_hash = '{0}[{1}]{2}'.format(
            self.fbasename, self.fhash, self.ext,
        )

    #############################################
    # subclass may override following methods.  #
    #############################################
    def init(self):
        pass

    #############################################
    # subclass must override following methods. #
    #############################################
    def generate_file_hash(self, data):
        raise NotImplementedError

    def list_remote(self):
        raise NotImplementedError

    def create_file(self):
        raise NotImplementedError

    def update_file(self, old_fhash):
        raise NotImplementedError

    def resource_url(self, fname, hash_tag):
        raise NotImplementedError
