import os
import time
import sqlalchemy


def before_all(context):
    """For LOCAL_BEHAVE you need to setup the environment manually"""

    context.SERVER_ADDRESS = 'localhost:8080'

    if os.environ['LOCAL_BEHAVE'] is None:
        # set environment
        os.environ['DATABASE_URI'] = 'postgresql://postgres:postgres@127.0.0.1:5432/deeptracy_test'
        os.environ['BROKER_URI'] = 'redis://127.0.0.1:6379/1'
        os.environ['SERVER_ADDRESS'] = context.SERVER_ADDRESS
        os.environ['GUNICORN_WORKERS'] = '1'

        os.system('docker-compose -f tests/acceptance/docker-compose.yml rm -f')
        os.system('docker-compose -f tests/acceptance/docker-compose.yml -p deeptracy_acceptance up -d --build')
        time.sleep(5)

    context.engine = sqlalchemy.create_engine(os.environ['DATABASE_URI'])


def after_all(context):
    if os.environ['LOCAL_BEHAVE'] is None:
        os.system('docker-compose -f tests/acceptance/docker-compose.yml kill')
        os.system('docker-compose -f tests/acceptance/docker-compose.yml rm -f')
