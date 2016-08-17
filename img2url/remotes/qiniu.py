# -*- coding: utf-8 -*-
from __future__ import (
    division, absolute_import, print_function, unicode_literals,
)
from builtins import *                  # noqa
from future.builtins.disabled import *  # noqa

from cStringIO import StringIO

from .base import REQUIRED_FIELD, Configuration, OperationPackage

from qiniu import Auth, BucketManager, put_file
from qiniu.utils import etag_stream


class QiniuConfig(Configuration):

    FIELDS = [
        ('qiniu_access_key', REQUIRED_FIELD),
        ('qiniu_secret_key', REQUIRED_FIELD),
        ('qiniu_bucket', REQUIRED_FIELD),
        ('qiniu_base_url', REQUIRED_FIELD),
    ]

    def postprocess_fields(self):
        base_url = self.fields['qiniu_base_url']
        if not base_url.endswith('/'):
            base_url += '/'
        if not base_url.startswith('http'):
            base_url = 'http://' + base_url
        self.fields['qiniu_base_url'] = base_url


class QiniuOperation(OperationPackage):

    def init(self):
        self.q = Auth(
            self.get_config('qiniu_access_key'),
            self.get_config('qiniu_secret_key'),
        )
        self.bucket = BucketManager(self.q)

    def token(self, filename):
        return self.q.upload_token(
            self.get_config('qiniu_bucket'),
            filename,
        )

    def generate_file_hash(self, data):
        fhash = etag_stream(StringIO(data))
        if isinstance(fhash, bytes):
            fhash = fhash.decode('ascii')
        return fhash

    def list_remote(self):
        rep = self.bucket.list(self.get_config('qiniu_bucket'))
        assert rep[1]
        ret = []
        for element in rep[0]['items']:
            ret.append(
                (element['key'], element['hash']),
            )
        return ret

    def create_file(self):
        token = self.token(self.fname)
        put_file(token, self.fname, self.fpath)
        return self.fname

    def update_file(self, old_fhash):
        token = self.token(self.fname_with_hash)
        put_file(token, self.fname_with_hash, self.fpath)
        return self.fname_with_hash

    def resource_url(self, fname, hash_tag):
        return self.get_config('qiniu_base_url') + fname
