# -*- coding: utf-8 -*-
"""
test_deptracy
----------------------------------
Tests for `deptracy` module.
"""


import pytest

from deptracy import deptracy


@pytest.fixture
def response():
    """
    Sample pytest fixture.
    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    return 'response'


def test_content(response):
    """
    Sample pytest test function with the pytest fixture as an argument.
    """
    deptracy.do_something()
    assert response is 'response'
