#from bottle import run
import os

from holeio import views  # noqa
from holeio import watcher, downloader, db

import logging
logger = logging.getLogger(__name__)

if os.path.isfile('holeio.cfg'):
  #config = ConfigParser.ConfigParser()
  #config.read('holeio.cfg')
  watcher.start_watching()
  downloader.start()

logging.debug("DEBUG logging visible")
logging.info("INFO logging visible")
logging.warning("WARNING logging visible")
db.add_history("Starting hole.io")
