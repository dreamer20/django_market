#!/bin/bash

if [ "$initial" = true ]; then
    echo "Start database migration."
    until python3 manage.py migrate
    do
        echo "Wait 3 seconds to try migration again."
        sleep 3
    done
    python3 manage.py loaddata data.json
fi
gunicorn -b '0.0.0.0:8000' project.wsgi