# -*- coding: utf-8 -*-
"""
test_app
----------------------------------
Tests for `deptracy.app` module.
"""

from unittest.mock import patch

from deptracy.app import sample_endpoint


def test_sample_endpoint():
    body, status_code = sample_endpoint()
    assert status_code == 200

