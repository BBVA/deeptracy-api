# -*- coding: utf-8 -*-

import logging
from json import dumps

from flask import Flask

app = Flask(__name__)

logger = logging.getLogger("deptracy")
logger.setLevel(logging.DEBUG)


@app.route("/")
def sample_endpoint():
    """
    Sample endpoint returns Hello: Worl
    :return:
    """
    logger.debug("Entering the sample_endpoint Service")
    return dumps({"Hello": "World"}), 200
