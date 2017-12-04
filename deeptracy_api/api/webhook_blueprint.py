# Copyright 2017 BBVA
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Blueprint for webhook endpoints"""

import logging

from flask import Blueprint, request

from ..webhook.parse import handle_github_webhook, handle_bitbucket_webhook

logger = logging.getLogger('deeptracy')

webhook = Blueprint('webhook', __name__)


@webhook.route('/', methods=["POST", "PUT"])
def receive_hook():
    """Receive a webhook and handle it

    Webhooks can be received from GitHub or fro BitBucket. This endpoint examines the request headers
    and decides if the data should be processed as a GitHub or as a BitBucket event.

    If the data is valid, a webhook can end if a project creation, a scan launch or both

    :return codes:  200 on success
                    400 on errors
    """
    # TODO: securize endpoint. This public endpoint should be securized
    if request.headers.get('X-Bitbucket-Type', None) is not None:
        logger.debug('received request to process a webhook from bitbucket')
        handle_bitbucket_webhook(request.headers, request.get_json())
    elif request.headers.get('X-GitHub-Event', None) is not None:
        logger.debug('received request to process a webhook from github')
        handle_github_webhook(request.headers, request.get_json())
    else:
        logger.debug('received unparseable webhook post')
        return '', 400

    return '', 200
