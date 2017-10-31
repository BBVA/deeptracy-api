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

import logging
import traceback

from flask import Flask, json, request
from flask_cors import CORS

from .project_blueprint import project
from .scan_blueprint import scan
from .webhook_blueprint import webhook
from .exc import APIError

logger = logging.getLogger('deeptracy')


def setup_api():
    flask_app = Flask('deeptracy_api')
    CORS(flask_app)

    load_blueprints(flask_app)

    # Register error handler for custom DeeptracyException exception
    @flask_app.errorhandler(APIError)
    def handle_invalid_usage(error):
        """
        Handler for APIErrors thrown by API endpoints
        """
        response = json.jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @flask_app.after_request
    def after_request(response):
        # This IF avoids the duplication of registry in the log,
        # since that 500 is already logged via @flask_app.errorhandler.
        if response.status_code != 500:
            logger.info('%s %s %s %s %s',
                         request.remote_addr,
                         request.method,
                         request.scheme,
                         request.full_path,
                         response.status)
        return response

    @flask_app.errorhandler(Exception)
    def exceptions(e):
        tb = traceback.format_exc()
        logger.error('%s %s %s %s 5xx INTERNAL SERVER ERROR\n%s',
                     request.remote_addr,
                     request.method,
                     request.scheme,
                     request.full_path,
                     tb)

        response = json.jsonify({'error': 'unexpected', 'status_code': 500})
        return response

    return flask_app


def load_blueprints(flask_app):
    # Register blueprints
    root = '/api/'
    prev1 = root + '1'

    flask_app.register_blueprint(webhook, url_prefix=prev1 + '/webhook')
    flask_app.register_blueprint(project, url_prefix=prev1 + '/project')
    flask_app.register_blueprint(scan, url_prefix=prev1 + '/scan')
