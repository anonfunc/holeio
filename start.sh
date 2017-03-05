#!/bin/bash

if [[ -d venv ]]
then
  source venv/bin/activate
  bottle.py -b 0.0.0.0:8080 holeio.app
else
  echo "Please run install.sh first"
  exit 1
fi

