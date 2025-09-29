#!/bin/bash

while true; do
  echo "Hello world" >> logs/cron.log 2>&1
  sleep 3
done
