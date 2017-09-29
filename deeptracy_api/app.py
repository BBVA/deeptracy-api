# -*- coding: utf-8 -*-
"""
Module for deeptracy
"""
from deeptracy_core.dal.database import db
from deeptracy_api.celery import setup_celery
from deeptracy_api.api.flask import setup_api

db.init_engine()  # Init database engine
celery = setup_celery()  # setup the celery client

flask_app = setup_api()  # setup flask api
