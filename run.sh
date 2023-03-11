#!/bin/sh
set -e
BIND_PORT="${PORT:-8080}"
BIND_ADDRESS="${ADDRESS:-0.0.0.0}"

if [ "$ENV" = 'DEV' ]; then
  echo "Running Development Server..."
  exec ADDRESS="$BIND_ADDRESS" python3 "run.py"
else
  echo "Running Production Server"
  echo "Binding to $BIND_ADDRESS:$BIND_PORT ..."
  exec uwsgi --plugins http,python --master --enable-threads --uid uwsgi --gid uwsgi --http "$BIND_ADDRESS":"$BIND_PORT" --wsgi-file run.py --callable app
fi