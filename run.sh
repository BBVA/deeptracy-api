#!/bin/bash

echo "run api in ${SERVER_ADDRESS}"

# Run the web
gunicorn -w ${GUNICORN_WORKERS} deeptracy_api.app:flask_app --bind ${SERVER_ADDRESS}
