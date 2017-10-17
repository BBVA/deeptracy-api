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

from deeptracy_api.api.webhook.bitbucket import parse_from_bitbucket
from deeptracy_api.api.webhook.github import parse_from_github


logger = logging.getLogger(__name__)


def parse_data(data):
    """
    Parse a JSON data payload from diferent repository providers.
    """
    if 'actor' in data \
            and 'links' in data['actor'] \
            and 'self' in data['actor']['links'] \
            and 'href' in data['actor']['links']['self'] \
            and 'bitbucket' in data['actor']['links']['self']['href']:
        logger.debug("BitBucket")
        return parse_from_bitbucket(data)
    elif 'repository' in data and 'url' in data['repository']:
        logger.debug("GitHub")
        return parse_from_github(data)
    else:
        return []
