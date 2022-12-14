#!/bin/sh

echo "Waiting for Mongo..."
while ! nc -z -v $MONGO_HOST $MONGO_PORT;
do
  >&2 echo "Mongo is unavailable - sleeping"
  sleep 0.4;
done
echo "Mongo was started"


exec "$@"