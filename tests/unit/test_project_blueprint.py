# Copyright 2017 BBVA
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json

from flask import url_for
from flask.testing import FlaskClient

from unittest import mock, TestCase
from deeptracy_api.api.flask import setup_api

from . import utils


class MockClient(FlaskClient):
    def open(self, *args, **kwargs):
        if 'json' in kwargs:
            kwargs['data'] = json.dumps(kwargs.pop('json'))
            kwargs['content_type'] = 'application/json'
        return super(MockClient, self).open(*args, **kwargs)


@mock.patch('deeptracy_api.api.project_blueprint.db.session_scope')
class ProjectBlueprintTestCase(TestCase):
    def setUp(self):
        app = setup_api()
        app.config['SERVER_NAME'] = 'localhost'
        app.test_client_class = MockClient
        app.testing = True
        ctx = app.app_context()
        ctx.push()
        self.app = app
        self.client = app.test_client()

    def test_post_project_without_data(self, mock_session):
        url = url_for('project.post_project')

        with self.app.test_request_context(url):
            res = self.client.post(url)
            msg = utils.get_msg_from_api_error(res)
            self.assertEqual(res.status_code, 400)
            self.assertEqual('invalid payload', msg)

    def test_patch_project_email_without_email(self, mock_session):
        url = url_for('project.patch_project_email', project_id='3')

        with self.app.test_request_context(url):
            res = self.client.patch(url)
            msg = utils.get_msg_from_api_error(res)
            self.assertEqual(res.status_code, 400)
            self.assertEqual('invalid payload', msg)
