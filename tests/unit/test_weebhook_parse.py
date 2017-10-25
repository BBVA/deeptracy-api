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

import json
import pytest
from unittest import mock, TestCase
from deeptracy_api.webhook.parse import handle_github_webhook, handle_bitbucket_webhook, add_scan_for_project_with_repo
from deeptracy_api.api.exc.exceptions import APIError


class WebhookParseTestCase(TestCase):

    def test_handle_github_webhook_invalid_event(self):
        """When an invalid event is received, the method raises an APIError"""
        request_headers = {'X-GitHub-Event': 'invalid'}
        request_data = {}
        with pytest.raises(APIError) as excinfo:
            handle_github_webhook(request_headers, request_data)

        assert excinfo.value.status_code == 400

    @mock.patch('deeptracy_api.webhook.parse.add_scan_for_project_with_repo')
    def test_handle_github_webhook_push_event_invalid_repo_url(self, mock_add_scan_for_project_with_repo):
        with open('tests/unit/resources/github_push_webhook_payload.json') as github_webhook_payload_push_json:
            github_webhook_payload_push_data = json.load(github_webhook_payload_push_json)

        # remove the url from the json
        github_webhook_payload_push_data['repository'].pop('url')

        request_headers = {'X-GitHub-Event': 'push'}

        with pytest.raises(APIError) as excinfo:
            handle_github_webhook(request_headers, github_webhook_payload_push_data)

        assert excinfo.value.status_code == 400

    @mock.patch('deeptracy_api.webhook.parse.add_scan_for_project_with_repo')
    def test_handle_github_webhook_push_event(self, mock_add_scan_for_project_with_repo):
        with open('tests/unit/resources/github_push_webhook_payload.json') as github_webhook_payload_push_json:
            github_webhook_payload_push_data = json.load(github_webhook_payload_push_json)

        repo_url = 'repo_url'
        github_webhook_payload_push_data['repository']['url'] = repo_url

        request_headers = {'X-GitHub-Event': 'push'}
        handle_github_webhook(request_headers, github_webhook_payload_push_data)

        assert mock_add_scan_for_project_with_repo.called
        mock_add_scan_for_project_with_repo.assert_called_with(repo_url)

    def test_handle_bitbucket_webhook_invalid_event(self):
        """When an invalid event is received, the method raises an APIError"""
        request_headers = {'X-Event-Key': 'invalid'}
        request_data = {}
        with pytest.raises(APIError) as excinfo:
            handle_bitbucket_webhook(request_headers, request_data)

        assert excinfo.value.status_code == 400

    @mock.patch('deeptracy_api.webhook.parse.add_scan_for_project_with_repo')
    def test_handle_github_webhook_push_event(self, mock_add_scan_for_project_with_repo):
        with open('tests/unit/resources/bitbucket_push_webhook_payload.json') as bitbucket_webhook_payload_push_json:
            bitbucket_webhook_payload_push_data = json.load(bitbucket_webhook_payload_push_json)

        repo_url = 'https://some.bitbucket-domain.com/project/repo'
        _self = {'href': repo_url}
        bitbucket_webhook_payload_push_data['repository']['links']['self'] = [_self]
        bitbucket_webhook_payload_push_data['repository']['fullName'] = 'project/repo'
        request_headers = {'X-Event-Key': 'repo:push'}
        handle_bitbucket_webhook(request_headers, bitbucket_webhook_payload_push_data)

        repo_url = 'ssh://git@some.bitbucket-domain.com:7999/project/repo.git'

        assert mock_add_scan_for_project_with_repo.called
        mock_add_scan_for_project_with_repo.assert_called_with(repo_url)
