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
    assert('canon_url' in response_data)
    assert('commits' in response_data)
    assert('repository' in response_data)
    response = {}

    for commit in response_data['commits']:
        branch_name = commit.get('branch')

        # In BitBucket, a branch value can be null. This can happen if a push
        # affects multiple branches (a variable 'branches' appears and the
        # 'branch' is set to empty). It also appears to happen when multiple
        # commits are pushed.
        if not branch_name:
            continue

        webhook = response.setdefault(branch_name, WebHookData('bitbucket'))
        repo = response_data['repository']
        webhook.repo_name = repo['slug']
        webhook.repo_url = "%s:%s/%s.git" % \
            (settings.PROVIDERS['bitbucket']['ssh_account'],
             repo['owner'], repo['slug'])
        webhook.ref_name = 'refs/heads/%s' % commit['branch']
        webhook.branch_name = branch_name
        if webhook.before is None:
            webhook.before = commit['raw_node'] + "^1"
        webhook.after = commit['raw_node']

    return response.values()
