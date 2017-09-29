from sqlalchemy import text
from behave import given, then

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

