from behave import given, when, then
from deeptracy_core.dal.database import db


@given(u'there are no projects in the database')
def step_impl(context):
    pass


@when(u'the user makes a "{method}" request to "{endpoint}" endpoint with {payload}')
def step_impl(context, method, endpoint, payload):
    pass


@then(u'the api response code is {response_code}')
def step_impl(context, response_code):
    pass


@then(u'the api response payload is {response}')
def step_impl(context, response):
    pass


@then(u'the new project is created in the database if the response is 201')
def step_impl(context):
    pass
