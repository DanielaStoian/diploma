#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py flush --no-input
python manage.py makemigrations
python manage.py migrate
python populate_dhmoi.py
cd scrapper/stations_scrapper
scrapy crawl BlinkCharging
scrapy crawl ElpeFuture
scrapy crawl PlugShare
scrapy crawl ProtergiaCharge
scrapy crawl Fortisis
scrapy crawl ChargeSpot
cd ../../

exec "$@"