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
from celery import Celery

from deeptracy_core.dal.project.manager import get_project_by_repo
from deeptracy_core.dal.scan.manager import add_scan
from deeptracy_core.dal.database import db
from deeptracy_api.config import BROKER_URI

logger = logging.getLogger(__name__)


def parse_data(request_headers, data) -> str:
    """
    Parse a JSON data payload from different repository providers.

    It returns the project repo url.

    :param request_headers: (dict) headers from the webhook
    :param data: (dict) data from the webhook

    :rtype: str
    :raises ValueError: On invalid project_id or in not found Project
    """
    if request_headers.get('X-Bitbucket-Type', None) is not None:
        if request_headers.get('X-Event-Key') == 'repo:push':
            # action for bitbucket repository push
            # TODO: bitbucket has various api versions
            # TODO: we are hardcoding the cloning repo template (with ssh)
            # TODO: handle errors in data traversing
            domain = data.get('repository').get('links').get('self')[0].get('href').split('/')[2]
            repo_fullname = data.get('repository').get('fullName').lower()
            repo = 'ssh://git@{domain}:7999/{repo_fullname}.git'.format(
                domain=domain,
                repo_fullname=repo_fullname
            )
            return repo
        else:
            return None
    else:
        logger.debug('invalid hook received')
        return None


def handle_data(request_headers, request_data):
    """
    Handle data incomming from webhook for PUSHES actions in project repositories

    If a valid data can be parsed from the webhook requests and a project is found matching
    the repo url extracted from the data, create a scan and send it to celery

    :param request_headers:
    :param request_data:
    :return:
    """
    repo = parse_data(request_headers, request_data)

    if repo is not None:
        logger.debug('repo from webhook {}'.format(repo))
        with db.session_scope() as session:
            project = get_project_by_repo(repo, session)
            # TODO: Do not hardcode the language, extract it from the project default_language
            # https://github.com/BBVA/deeptracy/issues/8
            lang = 'nodejs'
            scan = add_scan(project.id, lang, session)
            session.commit()

            celery = Celery('deeptracy', broker=BROKER_URI)
            celery.send_task("start_scan", [scan.id])
    else:
        logger.debug('webhook data cannot be parsed')
