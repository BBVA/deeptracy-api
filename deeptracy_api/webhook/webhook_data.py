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

from deeptracy_api.webhook.parse import parse_data

logger = logging.getLogger(__name__)


class WebHookData():
    def __init__(self, provider):
        self.provider = provider
        self.before = None
        self.after = None
        self.repo_name = None
        self.ref_name = None
        self.branch_name = None
        self.repo_url = None

    def get_provider(self):
        return self.provider

    def get_repository_name(self):
        return self.repo_name

    def get_before_sha(self):
        return self.before

    def get_after_sha(self):
        return self.after

    def get_ref(self):
        return self.ref_name

    def is_tag(self):
        return (self.ref_name.find('refs/tags/') == 0)


def handle_data(response_data):
    """
    Automatically parse the JSON data received and dispatch the requests
    to the appropriate handlers specified in settings.py.
    """
    data_list = parse_data(response_data)
    logger.debug("raw data %s" % data_list)

    for parsed_data in data_list:
        provider_info = settings.PROVIDERS.get(parsed_data.provider, None)

        if provider_info:
            handler = provider_info.get('post_receive_handler', None)
            if handler:
                handler(parsed_data)
