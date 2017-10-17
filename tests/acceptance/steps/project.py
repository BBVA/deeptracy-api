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
from behave import given, then, when

from tests.acceptance.utils import clean_db


@given(u'an empty project table in database')
def step_impl(context):
    clean_db(context)


@then(u'{created} projects are in the database')
def step_impl(context, created):
    sql = text('SELECT * FROM project')
    results = context.engine.execute(sql).fetchall()

    assert len(results) == int(created)


@given(u'a database with a project created')
def step_impl(context):
    sql = text('DELETE FROM project')
    context.engine.execute(sql)


@when(u'a project with id "{project_id}" exists in the database')
def step_impl(context, project_id):
    sql = text('INSERT INTO project (id, repo, hook_data, hook_type, repo_auth_type) '
               'VALUES (:id, :repo, :hook_data, :hook_type, :repo_auth_type)')
    context.engine.execute(sql,
                           id=project_id,
                           repo='http://test{}.com'.format(project_id),
                           hook_type='NONE',
                           hook_data='',
                           repo_auth_type='PUBLIC')


@then(u'project with id "{project_id}" is not in the database')
def step_impl(context, project_id):
    sql = text('SELECT * FROM project WHERE project.id = \'{}\''.format(project_id))
    results = context.engine.execute(sql).fetchall()

    assert len(results) == 0


@then(u'table projects is empty')
def step_impl(context):
    sql = text('SELECT * FROM project')
    results = context.engine.execute(sql).fetchall()

    assert len(results) == 0


@when(u'the user makes a "{method}" request to "/api/1/project/" endpoint')
def step_impl(context):
    raise NotImplementedError(u'STEP: When the user makes a "DELETE" request to "/api/1/project/" endpoint')


@when(u'the user makes a "GET" request to "<endpoint>" endpoint')
def step_impl(context):
    raise NotImplementedError(u'STEP: When the user makes a "GET" request to "<endpoint>" endpoint')
