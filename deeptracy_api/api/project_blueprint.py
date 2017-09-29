# -*- coding: utf-8 -*-
"""Blueprint for project endpoints"""

from flask import Blueprint, request
from flask import jsonify
from deeptracy_core.dal.project.manager import add_project
from deeptracy_core.dal.database import db

from deeptracy_api.api.utils import api_error_response


project = Blueprint("project", __name__)


@project.route("/", methods=["POST"])
def post_project():
    """Adds a project to the database

    It receive a Project in the body as a json object and tries to create the project in the database

    Example:
        Body
        {"repo": "http://google.com"}

    :return codes:  201 on success
                    400 on errors
                    409 on a duplicate repo
    """

    data = request.get_json()
    if not data:
        return api_error_response('invalid payload'), 400

    repo = data.get('repo', None)
    if repo is None or repo == '':
        return api_error_response('missing repo'), 400

    session = db.Session()
    try:
        project = add_project(repo, session)
        session.commit()
    except Exception as exc:
        session.rollback()
        if 'unique constraint "project_repo_key"' in exc.args[0]:
            return api_error_response('unique constraint project repo {}'.format(repo)), 409
        else:
            return api_error_response(exc.args[0]), 400

    return jsonify(project.to_dict()), 201
