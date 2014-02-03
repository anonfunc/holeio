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
exec bottle.py holeio.app > holeio.log
