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

import pytest
from unittest import mock
from tests.unit.base_test import BaseDeeptracyTest
from deeptracy_api.webhook.parse import handle_github_webhook
from deeptracy_api.api.exc.exceptions import APIError


class WebhookParseTestCase(BaseDeeptracyTest):

    def test_handle_github_webhook_invalid_event(self):
        """When an invalid event is received, the method raises an APIError"""
        request_headers = {'X-GitHub-Event': 'invalid'}
        request_data = {}
        with pytest.raises(APIError) as excinfo:
            handle_github_webhook(request_headers, request_data)

        assert excinfo.value.status_code == 400

    def test_handle_github_webhook_push_event(self):
        """When an invalid event is received, the method raises an APIError"""
        request_headers = {'X-GitHub-Event': 'push'}
        request_data = {}
        repo = handle_github_webhook(request_headers, request_data)

        assert repo is not None
