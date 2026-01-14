#!/bin/bash

export APP_ENV="production"
export DB_HOST="localhost"

echo "Application Environment: $APP_ENV"
echo "Database Host: $DB_HOST"

if [ "$APP_ENV" == "production" ]; then
  echo "Running in production mode"
else
  echo "Running in development mode"
fi
