#!/usr/bin/env bash
set -e

HOST="$1"
PORT="$2"
shift 2
cmd="$@"

until nc -z -v -w30 $HOST $PORT
do
  echo "Waiting for $HOST:$PORT to be available..."
  sleep 1
done

exec $cmd

# set -e

# host="$1"
# shift
# cmd="$@"

# until nc -z "$host" 3306; do
#   >&2 echo "MySQL is unavailable - sleeping"
#   sleep 1
# done

# >&2 echo "MySQL is up - executing command"
# exec $cmd