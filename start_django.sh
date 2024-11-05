#!/bin/bash

if [ "$DATABASE" = "mysql" ]
then
    echo "Waiting for MySQL to start..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
        sleep 1  # Increasing sleep interval to give MySQL enough time
    done
    
    echo "MySQL started"
fi

echo "Applying database migrations..."
sleep 10  # Additional wait time for MySQL readiness

python MovieDB/manage.py makemigrations
python MovieDB/manage.py migrate

echo "Starting Django server..."
python MovieDB/manage.py runserver 0.0.0.0:8000
