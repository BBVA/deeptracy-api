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

import os
import time
import sqlalchemy
import redis

from urllib.parse import urlparse


def before_all(context):
    """For LOCAL_BEHAVE you need to setup the environment manually"""

    if os.environ.get('LOCAL_BEHAVE', None) is None:
        # set environment
        os.environ['DATABASE_URI'] = 'postgresql://postgres:postgres@127.0.0.1:5433/deeptracy_test'
        os.environ['BROKER_URI'] = 'redis://127.0.0.1:6379'
        os.environ['SERVER_ADDRESS'] = '127.0.0.1:8080'
        os.environ['GUNICORN_WORKERS'] = '1'

        os.system('docker-compose -f tests/acceptance/docker-compose.yml rm -f')
        os.system('docker-compose -f tests/acceptance/docker-compose.yml up -d --build')
        time.sleep(10)

    context.SERVER_ADDRESS = os.environ['SERVER_ADDRESS']
    context.BROKER_URI = os.environ['BROKER_URI']

    context.engine = sqlalchemy.create_engine(os.environ['DATABASE_URI'])
    context.redis_db = _setup_redis(context.BROKER_URI)


def after_all(context):
    if os.environ.get('LOCAL_BEHAVE', None) is None:
        os.system('docker-compose -f tests/acceptance/docker-compose.yml stop')
        os.system('docker-compose -f tests/acceptance/docker-compose.yml rm -f')


def _setup_redis(uri: dict) -> redis.StrictRedis:
    _, netloc, path, _, _, _ = urlparse(uri)

    host, port = netloc.split(":", maxsplit=1)

    if not path:
        path = 0

    redis_db = redis.StrictRedis(host=host,
                                 port=port,
                                 db=path)

    return redis_db
