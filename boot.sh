#!/bin/bash
source venv/bin/activate
flask init_db
flask populate_db_test
exec gunicorn -b :5000 --access-logfile - --error-logfile - app_source:app
