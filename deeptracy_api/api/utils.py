# -*- coding: utf-8 -*-
"""Utils to be used in the API"""
from flask import jsonify


def api_error_response(msg: str):
    """Returns a json representation of an API error

    :param msg: Message to be returned
    """
    return jsonify({'error': {'msg': msg}})
