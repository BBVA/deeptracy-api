# -*- coding: utf-8 -*-
"""Utils to be used in the API"""
from flask import jsonify
from deeptracy_api.api.exc import APIError


def api_error_response(msg: str):
    """Returns a json representation of an API error

    :param msg: Message to be returned
    """
    return jsonify({'error': {'msg': msg}})


def get_required_field(data: dict, field: str):
    """Checks a required field in a dictionary that comes from a request
    If the field is not present or is '', raises an APIError

    :param data: Dictionary to check for the field
    :param field: Field key to check

    :raises APIError: on not found or empty field
    :rtype value: field value if the field is found in the dictionary
    """
    field_value = data.get(field, None)
    if field_value is None or field_value == '':
        raise APIError('missing {}'.format(field), status_code=400)
    return field_value
