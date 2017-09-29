# -*- coding: utf-8 -*-
"""Blueprint for scan endpoints"""
from celery import Celery
from flask import Blueprint, request
from flask import jsonify
from deeptracy_core.dal.scan.manager import add_scan
from deeptracy_core.dal.database import db

from deeptracy_api.config import BROKER_URI
from deeptracy_api.api.utils import api_error_response, get_required_field


scan = Blueprint("scan", __name__)


@scan.route("/", methods=["POST"])
def post_scan():
    with db.session_scope() as session:
        data = request.get_json()
        if not data:
            return api_error_response('invalid payload'), 400

        project_id = get_required_field(data, 'project_id')
        lang = get_required_field(data, 'lang')

        scan = add_scan(project_id, lang, session)
        session.commit()

        # when the scan is added to the database, a celery task is inserted for that scan to start the process
        celery = Celery('deeptracy', broker=BROKER_URI, backend=BROKER_URI)
        celery.send_task("start_scan", [scan.id])

        return jsonify(scan.to_dict()), 201
