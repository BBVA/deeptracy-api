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


def on_bitbucket_commit():
    print('---- bitbucket_commit ----')


def on_bitbucket_create():
    print('---- bitbucket_create ----')


def on_github_commit():
    print('---- github_commit ----')


def on_github_create():
    print('---- github_create ----')
