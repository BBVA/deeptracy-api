# -*- coding: utf-8 -*-

from flask import Blueprint, request, Response, json
from flask import jsonify
from deeptracy_core.dal.project.manager import get_project_list, add_project
from deeptracy_core.dal.database import db


project = Blueprint("project", __name__)


def api_error(msg: str):
    return jsonify({'error': {'msg': msg}})


@project.route("/", methods=["GET"])
def get_project():
    with db.session_scope() as session:
        project_list = get_project_list(session)
        return jsonify([item.to_dict() for item in project_list]), 200


@project.route("/", methods=["POST"])
def post_project():

    data = request.get_json()
    if not data:
        return api_error('invalid payload'), 400

    repo = data.get('repo', None)
    if repo is None or repo == '':
        return api_error('missing repo'), 400

    session = db.Session()
    try:
        project = add_project(repo, session)
        session.commit()
    except Exception as exc:
        session.rollback()
        if 'unique constraint "project_repo_key"' in exc.args[0]:
            return api_error('unique constraint project repo {}'.format(repo)), 409
        else:
            return api_error(exc.args[0]), 400

    return jsonify(project.to_dict()), 201
