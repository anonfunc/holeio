#!/bin/bash

if [[ -d venv ]]
then
  source venv/bin/activate
  nohup bottle.py -b 0.0.0.0:8080 holeio.app >> holeio.log &
else
  echo "Please run install.sh first"
  exit 1
fi

