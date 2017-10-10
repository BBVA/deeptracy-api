# Copyright 2017 BBVA
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""tests for DeeptracyException class"""

import pytest

from deeptracy_api.api.exc.exceptions import APIError


def test_deeptracy_exception_holds_an_api_status_code():
    """Deeptracy exception class should holds an attribute
    to save the api status code to return in case of that exception"""
    status_code = 201
    with pytest.raises(APIError) as excinfo:
        raise APIError('custom message', status_code=status_code)

    assert excinfo.value.status_code == status_code


def test_deeptracy_exception_holds_a_message():
    """Deeptracy exception class should holds a message"""
    msg = 'custom message'
    with pytest.raises(APIError) as excinfo:
        raise APIError(msg)

    assert msg in str(excinfo.value)
