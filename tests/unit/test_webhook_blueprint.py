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

from flask import url_for
from unittest import mock, TestCase
from deeptracy_api.api.flask import setup_api


class WebhookBlueprintTestCase(TestCase):
    def setUp(self):
        app = setup_api()
        app.config['SERVER_NAME'] = 'localhost'
        app.testing = True
        ctx = app.app_context()
        ctx.push()
        self.app = app
        self.client = app.test_client()

    @mock.patch('deeptracy_api.api.webhook_blueprint.handle_bitbucket_webhook')
    def test_receive_bitbucket_webhook(self, mock_handle_bitbucket_webhook):
        """When the api receive a Bitbucket webhook it should call the Bitbucket webhook parser"""
        url = url_for("webhook.receive_hook")

        with self.app.test_request_context(url):
            self.client.post(url, headers={'X-Bitbucket-Type': 'event:push'})
            assert mock_handle_bitbucket_webhook.called

    @mock.patch('deeptracy_api.api.webhook_blueprint.handle_github_webhook')
    def test_receive_github_webhook(self, mock_handle_github_webhook):
        """When the api receive a github webhook it should call the github webhook parser"""
        url = url_for("webhook.receive_hook")

        with self.app.test_request_context(url):
            self.client.post(url, headers={'X-GitHub-Event': 'event:push'})
            assert mock_handle_github_webhook.called

    @mock.patch('deeptracy_api.api.webhook_blueprint.handle_github_webhook')
    def test_receive_invlaid_webhook(self, mock_handle_github_webhook):
        """When the api receive a post without a valid header, it returns a 400 code"""
        url = url_for("webhook.receive_hook")

        with self.app.test_request_context(url):
            res = self.client.post(url, headers={'invalid': 'event:push'})
            assert res.status_code == 400
