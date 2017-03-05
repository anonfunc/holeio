#!/bin/bash
#set -x
if [[ ! -d venv ]]
then
  # Path is for synology nas
  # /volume1/@appstore/python/bin/virtualenv venv
  if hash virtualenv 2> /dev/null
  then
    virtualenv venv
  else
    echo 'virtualenv tool is not installed.  See https://virtualenv.pypa.io/en/stable/installation/'
    exit 1
  fi
fi
source venv/bin/activate
pip install -r requirements.txt
python setup.py develop
echo 'Development environment created.  To start the application:'
echo 'source venv/bin/activate'
echo 'bottle.py -b 0.0.0.0:8080 holeio.app 2>&1 > holeio.log &'
