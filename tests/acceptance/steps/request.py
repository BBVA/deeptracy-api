import requests
from flask import json
from behave import when, then


@when(u'the user makes a "{method}" request to "{endpoint}" endpoint with {payload}')
def step_impl(context, method, endpoint, payload):
    endpoint = 'http://{}{}'.format(context.SERVER_ADDRESS, endpoint)
    res = requests.request(method, endpoint, json=json.loads(payload))
    context.last_response = res


@then(u'the api response code is {response_code}')
def step_impl(context, response_code):
    json_data = context.last_response.text

    assert context.last_response.status_code == int(response_code)


@then(u'the api response payload is {response}')
def step_impl(context, response):
    json_data = json.loads(context.last_response.text)

    json_expected = json.loads(response)

    context.last_project_id = json_data.get('id', None)

    # remove the id from response and expected result
    json_data.pop('id', None)
    json_expected.pop('id', None)
    assert json_data == json_expected
