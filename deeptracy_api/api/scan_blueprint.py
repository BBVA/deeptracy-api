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
    """Add a scan on the database

    Add a scan language on existing project

    Example:
        Body
        {
          "project_id": "00001",
          "lang": "javascript"
        }

    :return codes:  201 on success
                    400 on errors
    """
    with db.session_scope() as session:
        data = request.get_json()
        if not data:
            return api_error_response('invalid payload'), 400

        project_id = get_required_field(data, 'project_id')
        lang = data.get('lang', None)

        scan = add_scan(project_id, session, lang=lang)
        session.commit()

        # when the scan is added to the database, a celery task is inserted for that scan to start the process
        celery = Celery('deeptracy', broker=BROKER_URI)
        celery.send_task("start_scan", [scan.id])

        return jsonify(scan.to_dict()), 201
