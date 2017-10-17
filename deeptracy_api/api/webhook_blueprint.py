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

"""Blueprint for webhook endpoints"""

import logging

from flask import Blueprint, request

from deeptracy_api.webhook.parse import handle_data

logger = logging.getLogger(__name__)
webhook = Blueprint("webhook", __name__)


@webhook.route('/', methods=["POST"])
def index():
    """Repositorie Triggers

    Parse and launch triggers from an action on external repositories

    Example:

    :return codes:  201 on success
                    400 on errors
    """
    # TODO: securize endpoint. This public endpoint should be securized
    if request.json:
        logger.debug("received request to process a webhook")
        handle_data(request.headers, request.json)
    else:
        logger.debug("received unparseable webhook post")
        return '', 400

    return '', 200
