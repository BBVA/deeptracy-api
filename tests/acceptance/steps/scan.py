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

import uuid
from datetime import datetime, timedelta
from sqlalchemy import text
from behave import given, then, when


@given(u'a database ready to receive scans')
def step_impl(context):
    project_id = '123'
    plugin_lang = 'lang'

    sql = text('INSERT INTO project (id, repo) VALUES (:id, :repo)')
    context.engine.execute(sql, id=project_id, repo='http://test.com')

    sql = text('INSERT INTO plugin (id, name, lang, active) VALUES (:id, :name, :lang, :active)')
    context.engine.execute(sql, id='123', name='plugin', lang=plugin_lang, active=True)

    context.project_id = project_id
    context.plugin_lang = plugin_lang


@then(u'{created} scans are in the database')
def step_impl(context, created):
    sql = text('SELECT * FROM scan')
    results = context.engine.execute(sql).fetchall()

    assert len(results) == int(created)


@given(u'a scan created {minutes} mins ago exists in the database for a project')
def step_impl(context, minutes):
    scan_id = uuid.uuid4().hex
    created = datetime.now() - timedelta(minutes=int(minutes))
    sql = text('INSERT INTO scan (id, project_id, created) VALUES (:id, :project_id, :created)')
    context.engine.execute(sql, id=scan_id, project_id=context.project_id, created=created)


@when(u'a scan with id "{scan_id}" exists in the database')
def step_impl(context, scan_id):
    sql = text('SELECT * FROM scan WHERE scan.id = \'{}\''.format(scan_id))
    results = context.engine.execute(sql).fetchall()

    assert len(results) == 0


@when(u'the scan with id {scan_id} has vulnerabilities')
def step_impl(context, scan_id):
    scan_id_str= '0000001'
    vulnerability_id = uuid.uuid4().hex
    library = "tar"
    version = "1.0.3"
    severity = "1"
    summary = ""
    advisory = ""

    created = datetime.now() - timedelta(minutes=3)
    sql = text('INSERT INTO scan (id, project_id, created) VALUES (:id, :project_id, :created)')
    context.engine.execute(sql, id=scan_id_str, project_id=context.project_id, created=created)

    sql = text('INSERT INTO scan_vulnerability (id, scan_id, library, version, severity, summary, advisory) '
               'VALUES (:id, :scan_id, :library, :version, :severity, :summary, :advisory)')
    context.engine.execute(sql, id=vulnerability_id, scan_id=scan_id_str, library=library, version=version,
                           severity=severity, summary=summary, advisory=advisory)
