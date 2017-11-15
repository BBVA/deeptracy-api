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
from deeptracy_core.dal.scan.manager import add_scan, get_num_scans_in_last_minutes
from deeptracy_core.dal.database import db

from ..config import BROKER_URI, ALLOWED_SCANS_PER_PERIOD, ALLOWED_SCANS_CHECK_PERIOD
from ..api.exc.exceptions import APIError

logger = logging.getLogger('deeptracy')


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


def handle_github_webhook(request_headers, request_data):
    """
    Get headers and data received in a github webhook

    Only process push events and raise an APIError in other events.
    Examine X-GitHub-Event header and if a push event is received,
    process it and extract the repo URL from it.

    Once we have the repo url add scan for the received project if
    a project with that repo exists

    :param request_headers: (dict) All headers received in the request
    :param request_data: (dict) Data received in the request
    :raises: APIError
    """
    if request_headers.get('X-GitHub-Event') == 'push':
        repository = request_data.get('repository', {})
        repo_url = repository.get('url', None)

        if repo_url is not None:
            add_scan_for_project_with_repo(repo_url)
        else:
            raise APIError('invalid repo', status_code=400)
    else:
        raise APIError('invalid event', status_code=400)


def handle_bitbucket_webhook(request_headers, request_data):
    """
    Get headers and data received in a Bitbucket webhook

    Only process push events and raise an APIError in other events.
    Examine X-Event-Key header and if a push event is received,
    process it and extract the repo URL from it.

    Once we have the repo url add scan for the received project if
    a project with that repo exists

    :param request_headers: (dict) All headers received in the request
    :param request_data: (dict) Data received in the request
    :raises: APIError
    """
    if request_headers.get('X-Event-Key') == 'repo:push':
        # TODO: bitbucket has various api versions
        # TODO: we are hardcoding the cloning repo template (with ssh)
        repository = request_data.get('repository', {})
        links = repository.get('links', {})
        self = links.get('self', [{}])
        href = self[0].get('href', None)
        repo_fullname = repository.get('fullName', None)

        if href is not None:
            # href should be https://some.bitbucket-domain.com/project/repo
            domain = href.split('/')[2]  # get domain (with subdomains)

        if repo_fullname is not None:
            repo_fullname = repo_fullname.lower()

        if href and repo_fullname is not None:
            repo_url = 'ssh://git@{domain}:7999/{repo_fullname}.git'.format(
                domain=domain,
                repo_fullname=repo_fullname
            )
            add_scan_for_project_with_repo(repo_url)
        else:
            raise APIError('invalid repo data', status_code=400)
    else:
        raise APIError('invalid event', status_code=400)


def add_scan_for_project_with_repo(repo_url: str):
    """
    If a project with repo_url exists in the database, adds a scan to it

    :param repo_url: (str) repo url for the project to launch the
    :return:
    """
    assert type(repo_url) is str

    with db.session_scope() as session:

        project = get_project_by_repo(repo_url, session)

        allowed_scan = True
        if ALLOWED_SCANS_PER_PERIOD > 0:
            previous_scans = get_num_scans_in_last_minutes(project.id, ALLOWED_SCANS_CHECK_PERIOD, session)
            allowed_scan = previous_scans < ALLOWED_SCANS_PER_PERIOD

        if allowed_scan:
            scan = add_scan(project.id, session)
            session.commit()

            celery = Celery('deeptracy', broker=BROKER_URI)
            celery.send_task('start_scan', [scan.id])
        else:
            raise APIError('cant create more scans', status_code=503)
