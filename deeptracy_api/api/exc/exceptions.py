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

"""
This module contains an object that represent an API Error

Any APIError thrown in an endpoint is handled to return to the user
a proper json error with custom status code and message
"""


class APIError(Exception):
    """
    Represents an API Error

    :param message: message to be returned to the user
    :param status_code: response status code (defaults to 400)
    :param payload: custom payload to give extra info in the response

    Example:
            >>> raise APIError('Error detected', 500, {'extra': 'extra_info'})

    """

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code or 400
        self.payload = payload

    def to_dict(self):
        """Convert exception to dict"""
        dict_ = dict(self.payload or ())
        dict_['msg'] = self.message
        return {'error': dict_}

    def __str__(self):
        return '[%d] %s' % (self.status_code, self.message)
