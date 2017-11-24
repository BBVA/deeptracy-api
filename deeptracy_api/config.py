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
import logging

from enum import Enum

BROKER_URI = os.environ.get('BROKER_URI')
DATABASE_URI = os.environ.get('DATABASE_URI')
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')

logger = logging.getLogger('deeptracy')


# config keys saved in database
class DbConfig(Enum):
    ALLOWED_SCANS_PER_PERIOD = 1
    ALLOWED_SCANS_CHECK_PERIOD = 5


def save_configs_to_database():
    """Some config properties should be saved in the database.

    If the config options are not saved in the database, save them
    """
    from deeptracy_core.dal.config.manager import get_config, save_config
    from deeptracy_core.dal.database import db

    for config in DbConfig:
        env_value = int(os.environ.get(config.name, config.value))
        with db.session_scope() as session:
            saved_value = get_config(config.name, session)
            if not saved_value:
                # adding a try avoid exceptions when multiple workers try to save the same key at the same time
                try:
                    save_config(config.name, env_value, session)
                except Exception:  # noqa
                    logger.debug('config key {} already exists'.format(config.name))
