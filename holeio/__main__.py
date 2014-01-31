from bottle import run
import os
import ConfigParser

from holeio import views  # noqa
from holeio import watcher, downloader

if os.path.isfile('holeio.cfg'):
  #config = ConfigParser.ConfigParser()
  #config.read('holeio.cfg')
  watcher.start_watching()
  downloader.start()
run(host='localhost', port=8080, reloader=True, debug=True)
