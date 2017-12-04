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

import requests
from flask import json
from behave import when, then
from jsondiff import diff


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
        [data.pop('created', None) for data in json_data]
        [data.pop('id', None) for data in json_expected]
        [data.pop('created', None) for data in json_expected]

    else:
        json_data.pop('id', None)
        json_data.pop('created', None)
        json_expected.pop('id', None)
        json_expected.pop('created', None)

    assert len(diff(json_data, json_expected)) == 0
