#!/bin/bash

THRESHOLD=80

echo "Disk Usage Report"

df -h | awk '{print $5 " " $1}' | while read output
do
  usage=$(echo $output | awk '{print $1}' | sed 's/%//g')
  partition=$(echo $output | awk '{print $2}')

  if [ "$usage" -ge "$THRESHOLD" ]; then
    echo "WARNING: Disk usage on $partition is above $THRESHOLD%"
  fi
done
