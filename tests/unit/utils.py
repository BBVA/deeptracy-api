import json


def get_msg_from_api_error(response):
    """
    checks when a response object has a valid APIError and return
    the message

    :param response:
    :return:
    """
    res_data = json.loads(response.data)
    assert response.status_code > 300
    error = res_data.get('error')
    assert type(error) is dict
    msg = error.get('msg')
    assert type(msg) is str
    return msg
