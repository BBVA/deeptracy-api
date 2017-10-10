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

from sqlalchemy import text


def clean_db(context):
    sql = text('DELETE FROM scan')
    context.engine.execute(sql)

    sql = text('DELETE FROM project')
    context.engine.execute(sql)

    sql = text('DELETE FROM plugin')
    context.engine.execute(sql)

    context.redis_db.delete('celery')
