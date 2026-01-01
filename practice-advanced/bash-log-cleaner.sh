#!/bin/bash

LOG_DIR="./logs"
ARCHIVE_DIR="./archive"

echo "Checking log directory..."

mkdir -p $ARCHIVE_DIR

for file in $LOG_DIR/*.log
do
  if [ -f "$file" ]; then
    echo "Archiving $file"
    mv "$file" "$ARCHIVE_DIR/"
  fi
done

echo "Log cleanup completed successfully."
