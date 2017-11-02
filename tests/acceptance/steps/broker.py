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

import json

from behave import then


@then(u'{created} celery tasks of type prepare_scan are in the broker')
def step_impl(context, created):
    created = int(created)

    # assert that only 1 task in the celery queue
    task_found = context.redis_db.llen('celery')
    assert task_found == created

    if created > 0:
        # get the task
        item = context.redis_db.lpop('celery')
        item = json.loads(item)
        headers = item.get('headers')

        # asserts the correct task is in the list
        assert headers.get('task') == 'prepare_scan'
