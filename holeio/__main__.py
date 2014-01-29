from bottle import run
import ConfigParser

from holeio import views  # noqa

config = ConfigParser.ConfigParser()
config.read('holeio.cfg')

run(host='localhost', port=8080, reloader=True, debug=True)
