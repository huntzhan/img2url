# -*- coding: utf-8 -*-
from __future__ import (
    division, absolute_import, print_function, unicode_literals,
)
from builtins import *                  # noqa
from future.builtins.disabled import *  # noqa

# remove following code.
from img2url.main import entry_point


def test_entry_point():
    assert 42 == entry_point()
