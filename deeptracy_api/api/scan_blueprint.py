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
import logging

from celery import Celery
from flask import Blueprint, request
from flask import jsonify
from deeptracy_core.dal.scan.manager import add_scan, get_num_scans_in_last_minutes, get_scan_vulnerabilities
from deeptracy_core.dal.scan_dep.manager import get_scan_dep_by_id
from deeptracy_core.dal.vulnerability.manager import get_vulns_for_cpe
from deeptracy_core.dal.project.manager import get_project
from deeptracy_core.dal.database import db

from ..config import BROKER_URI, ALLOWED_SCANS_PER_PERIOD, ALLOWED_SCANS_CHECK_PERIOD
from .utils import api_error_response, get_required_field

scan = Blueprint("scan", __name__)

logger = logging.getLogger('deeptracy')


@scan.route("/", methods=["POST"])
def post_scan():
    """Add a scan on the database

    Add a scan language on existing project

    Example:
        Body
        {
          "project_id": "00001",
          "lang": "javascript",
          "branch": "develop" //Optional
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

        branch = data.get('branch', None)
        if branch is None or branch == '':
            branch = 'master'
        else:
            project = get_project(project_id, session)
            command = 'git ls-remote --ref {}'.format(project.repo)

        # if defined, limit the number of scans that can be created by a given period for the same project
        logger.debug(' allowed scans per period {}/{}'.format(ALLOWED_SCANS_PER_PERIOD, ALLOWED_SCANS_CHECK_PERIOD))
        allowed_scan = True
        if ALLOWED_SCANS_PER_PERIOD > 0:
            previous_scans = get_num_scans_in_last_minutes(project_id, ALLOWED_SCANS_CHECK_PERIOD, session)
            allowed_scan = previous_scans < ALLOWED_SCANS_PER_PERIOD

        if allowed_scan:
            scan = add_scan(project_id, session, lang=lang, branch=branch)
            session.commit()

            # when the scan is added to the database, a celery task is inserted for that scan to start the process
            celery = Celery('deeptracy', broker=BROKER_URI)
            celery.send_task('prepare_scan', [scan.id])

            return jsonify(scan.to_dict()), 201
        else:
            return api_error_response('cant create more scans'), 403


@scan.route("/<string:scan_id>/vulnerabilities", methods=["GET"])
def get_vulnerabilities(scan_id):
    """Get scan vulnerabilities"""
    with db.session_scope() as session:
        try:
            scan_vulnerabilities = [scan_vulnerability.to_dict() for scan_vulnerability in get_scan_vulnerabilities(scan_id, session)]
            response = []

            def fillResponse(scan_vulnerability):
                vulns = get_vulns_for_cpe(scan_vulnerability['cpe'], session)
                scan_dep = get_scan_dep_by_id(scan_vulnerability['scan_dep_id'], session)
                return [response.append(
                    {
                        'library': scan_dep.library,
                        'version': scan_dep.version,
                        'cpe': vuln.cpe,
                        'cve': vuln.cve
                    }) for vuln in vulns]

            [ fillResponse(scan_vulnerability) for scan_vulnerability in scan_vulnerabilities]
        except Exception as exc:
            return api_error_response(exc.args[0]), 404

        return jsonify(response)
