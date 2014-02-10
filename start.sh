#!/opt/bin/bash
set -x
if [[ ! -d venv ]]
then
  # Path is for synology nas
  /volume1/@appstore/python/bin/virtualenv venv
fi
source venv/bin/activate
pip install -r requirements.txt
python setup.py develop
nohup bottle.py holeio.app 2>&1 > holeio.log &
