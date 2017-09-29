# -*- coding: utf-8 -*-

from flask import Flask, json
from flask_cors import CORS

from deeptracy_api.api.project_blueprint import project
from deeptracy_api.api.scan_blueprint import scan
from deeptracy_api.api.exc import APIError


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

    return flask_app


def load_blueprints(flask_app):
    # Register blueprints
    root = '/api/'
    prev1 = root + '1'

    flask_app.register_blueprint(project, url_prefix=prev1 + '/project')
    flask_app.register_blueprint(scan, url_prefix=prev1 + '/scan')
