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
    if request.method == 'POST':

        if request.json:
            # Most providers don't use JSON mime-types, but in case they do
            # handle it.
            logger.debug("Handling json")
            handle_data(request.json)
        elif 'payload' in request.form:
            logger.debug("Decoding payload: %s" % request.form['payload'])
            # BitBucket includes newlines in the message data; disable
            # strict checking
            json_data = json.loads(request.form['payload'], strict=False)
            handle_data(json_data)
        return "OK"
    return "OK"

