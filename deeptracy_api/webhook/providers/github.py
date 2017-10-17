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

from deeptracy_api.api.webhook import Hook

def parse_from_github(response_data):
    """
    Parses GitHub JSON WebHook response_data.  See:

    https://help.github.com/articles/post-receive-hooks
    """
    assert('before' in response_data)
    assert('after' in response_data)
    assert('repository' in response_data)
    assert('ref' in response_data)

    repo = response_data['repository']
    ref = response_data['ref']

    hook_data = Hook('github')
    hook_data.before = response_data['before']
    hook_data.after = response_data['after']
    hook_data.repo_name = response_data['repository']['name']
    hook_data.ref_name = ref
    hook_data.branch_name = ref.replace('refs/heads/', '')
    hook_data.repo_url = "%s:%s/%s.git" % \
        (settings.PROVIDERS['github']['ssh_account'],
         repo['owner']['name'], repo['name'])

    return [hook_data]
