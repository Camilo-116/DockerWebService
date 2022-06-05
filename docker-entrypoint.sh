#!/bin/sh -e

until nc -vz mysql-db:3306 > /dev/null; do
    >&2 echo "mysql-db:3306 is unavailable - sleeping"
    sleep 1
  done
  >&2 echo "mysql-db:3306 is up"

python3 -m flask run --host=0.0.0.0

exit 0
