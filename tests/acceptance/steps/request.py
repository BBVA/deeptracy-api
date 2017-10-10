import requests
from flask import json
from behave import when, then


@when(u'the user makes a "{method}" request to "{endpoint}" endpoint with {payload}')
def step_impl(context, method, endpoint, payload):
    endpoint = 'http://{}{}'.format(context.SERVER_ADDRESS, endpoint)
    if payload == 'empty':
        res = requests.request(method, endpoint)
    else:
        res = requests.request(method, endpoint, json=json.loads(payload))

    context.last_response = res


@then(u'the api response code is {response_code}')
def step_impl(context, response_code):
    assert context.last_response.status_code == int(response_code)


@then(u'the api response payload is {response}')
def step_impl(context, response):
    if response == 'empty':
        json_data = {}
        json_expected = {}
    else:
        json_data = json.loads(context.last_response.text)
        json_expected = json.loads(response)

    # remove the id from response and expected result
    if isinstance(json_data, list):
        [data.pop('id', None) for data in json_data]
    else:
        json_data.pop('id', None)
        json_expected.pop('id', None)

    assert json_data == json_expected
