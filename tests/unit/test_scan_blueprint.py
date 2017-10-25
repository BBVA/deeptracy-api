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
from deeptracy_core.dal.scan.model import Scan
from . import utils


class TestClient(FlaskClient):
    def open(self, *args, **kwargs):
        if 'json' in kwargs:
            kwargs['data'] = json.dumps(kwargs.pop('json'))
            kwargs['content_type'] = 'application/json'
        return super(TestClient, self).open(*args, **kwargs)


@mock.patch('deeptracy_api.api.scan_blueprint.db.session_scope')
class ScanBlueprintTestCase(TestCase):
    def setUp(self):
        app = setup_api()
        app.config['SERVER_NAME'] = 'localhost'
        app.test_client_class = TestClient
        app.testing = True
        ctx = app.app_context()
        ctx.push()
        self.app = app
        self.client = app.test_client()

    def test_post_scan_without_data(self, mock_session):
        url = url_for('scan.post_scan')

        with self.app.test_request_context(url):
            res = self.client.post(url)
            msg = utils.get_msg_from_api_error(res)
            self.assertEqual(res.status_code, 400)
            self.assertEqual('invalid payload', msg)

    def test_post_scan_without_project_id(self, mock_session):
        url = url_for('scan.post_scan')

        with self.app.test_request_context(url):
            res = self.client.post(url, json={'test': 2})
            msg = utils.get_msg_from_api_error(res)
            self.assertEqual(res.status_code, 400)
            self.assertEqual('missing project_id', msg)

    @mock.patch('deeptracy_api.api.scan_blueprint.Celery')
    @mock.patch('deeptracy_api.api.scan_blueprint.add_scan')
    def test_post_scan(self, mock_add_scan, mock_celery, mock_session):
        url = url_for('scan.post_scan')

        mock_add_scan.return_value = Scan(id='123')

        with self.app.test_request_context(url):
            res = self.client.post(url, json={'project_id': '12'})
            self.assertEqual(res.status_code, 201)
            mock_add_scan.assert_called_once_with('12', mock.ANY, lang=None)

    @mock.patch('deeptracy_api.api.scan_blueprint.Celery')
    @mock.patch('deeptracy_api.api.scan_blueprint.add_scan')
    def test_post_scan_with_lang(self, mock_add_scan, mock_celery, mock_session):
        url = url_for('scan.post_scan')

        mock_add_scan.return_value = Scan(id='123')

        with self.app.test_request_context(url):
            res = self.client.post(url, json={'project_id': '12', 'lang': 'nodejs'})
            self.assertEqual(res.status_code, 201)
            mock_add_scan.assert_called_once_with('12', mock.ANY, lang='nodejs')
