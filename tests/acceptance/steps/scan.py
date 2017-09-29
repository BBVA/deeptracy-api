from sqlalchemy import text
from behave import given, then
from tests.acceptance.utils import clean_db


@given(u'a database ready to receive scans')
def step_impl(context):
    project_id = '123'
    plugin_lang = 'lang'

    clean_db(context)

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
