from bottle import run
import ConfigParser

from holeio import views  # noqa
from holeio import watcher, downloader

config = ConfigParser.ConfigParser()
config.read('holeio.cfg')

watcher.start_watching()
downloader.start()
run(host='localhost', port=8080, reloader=True, debug=True)
