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

from deeptracy_api.webhook.webhook_data import WebHookData

def parse_from_bitbucket(response_data):
    """
    Parses BitBucket JSON WebHook response_data.  See:

    https://confluence.atlassian.com/display/BITBUCKET/POST+Service+Management
    """
    # assert('actor' in response_data)
    # assert('push' in response_data)
    # assert('repository' in response_data)
    response = {}

    if 'push' in response_data and 'changes' in response_data['push']:

        repo = response_data['repository']
        branch_name = response_data['push']['changes'][0]['new']['name']

        webhook = response.setdefault(branch_name, WebHookData('bitbucket'))

        webhook.repo_name = repo['name']
        webhook.repo_url = "%s:%s/%s.git" % \
            (settings.PROVIDERS['bitbucket']['ssh_account'],
             repo['owner'], repo['slug'])
        webhook.ref_name = 'refs/heads/%s' % branch_name
        webhook.branch_name = branch_name

    return response.values()
