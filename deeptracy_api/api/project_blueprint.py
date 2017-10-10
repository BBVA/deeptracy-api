# -*- coding: utf-8 -*-
"""Blueprint for project endpoints"""

from flask import Blueprint, request
from flask import jsonify, json
from deeptracy_core.dal.project.model import Project
import deeptracy_core.dal.project.manager as project_manager
from deeptracy_core.dal.database import db

from deeptracy_api.api.utils import api_error_response


project = Blueprint("project", __name__)


@project.route('/', methods=["POST"])
def add_project():
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
        project = project_manager.add_project(repo, session)
        session.commit()
    except Exception as exc:
        session.rollback()
        if 'unique constraint "project_repo_key"' in exc.args[0]:
            return api_error_response('unique constraint project repo {}'.format(repo)), 409
        else:
            return api_error_response(exc.args[0]), 400

    return jsonify(project.to_dict()), 201


@project.route('/<string:project_id>', methods=["GET"])
def get_project(project_id):
    session = db.Session()
    try:
        project = project_manager.get_project(project_id, session)
    except Exception as exc:
        if 'unique constraint "project_repo_key"' in exc.args[0]:
            return api_error_response('unique constraint project repo {}'.format(repo)), 409
        else:
            return api_error_response(exc.args[0]), 400

    return jsonify(project.to_dict()), 200


@project.route('/', methods=["GET"])
def get_projects():
    session = db.Session()
    try:
        rs = project_manager.get_projects(session)
    except Exception as exc:
        return api_error_response(exc.args[0]), 400

    projects = session.query(Project).all()
    projectArr = [project.to_dict() for project in projects]

    return jsonify(projectArr), 200



@project.route('/<string:project_id>', methods=["UPDATE"])
def update_project():
    """Updates a project on the database

    It receive a Project in the body as a json object and tries to create the project in the database

    Example:
        Body
        {"repo": "http://google.com"}

    :return codes:  201 on success
                    400 on errors
    """

    data = request.get_json()
    if not data:
        return api_error_response('invalid payload'), 400

    repo = data.get('repo', None)
    if repo is None or repo == '':
        return api_error_response('missing repo'), 400

    session = db.Session()
    try:
        project = project_manager.update_project(repo, session)
        session.commit()
    except Exception as exc:
        session.rollback()
        return api_error_response(exc.args[0]), 400

    return jsonify(project.to_dict()), 201

@project.route('/<string:project_id>', methods=["DELETE"])
def delete_project(project_id):
    """Remove a project on the database

    Tries to delete the project that you specified in the endpoint on the database

    :return codes:  204 on success (no content)
                    404 on errors (not found)
    """
    session = db.Session()
    project = session.query(Project).get(project_id)

    try:
        if project:
            project_manager.delete_project(project_id, session)
            session.commit()
        else:
            return api_error_response('project not found'), 404

    except Exception as exc:
        session.rollback()
        return api_error_response(exc.args[0]), 404

    return '', 204

@project.route('/', methods=["DELETE"])
def delete_projects():
    """Remove a project on the database

    Tries to delete the project that you specified in the endpoint on the database

    :return codes:  204 on success (no content)
                    400 on errors
    """
    session = db.Session()
    try:
        project_manager.delete_projects(session)
        session.commit()
    except Exception as exc:
        session.rollback()
        return api_error_response(exc.args[0]), 400

    return '', 204
