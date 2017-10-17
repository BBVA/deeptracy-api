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

import os
from deeptracy_api.triggers import on_github_commit, on_github_create, on_bitbucket_commit, on_bitbucket_create

BROKER_URI = os.environ.get('BROKER_URI')
DATABASE_URI = os.environ.get('DATABASE_URI')

PROVIDERS = {}

PROVIDERS['github'] = {
    'ssh_account' : 'git@github.com',
    'on_commit' : on_github_commit,
    'on_create': on_github_create
}

PROVIDERS['bitbucket'] = {
    'ssh_account' : 'git@bitbucket.org',
    'on_commit' : on_bitbucket_commit,
    'on_create' : on_bitbucket_create
}
