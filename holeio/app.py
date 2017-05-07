# from bottle import run
import ConfigParser
import os

from holeio import views  # noqa
from holeio import watcher, downloader, db

import logging
logger = logging.getLogger(__name__)

if os.path.isfile('holeio.cfg'):
    config = ConfigParser.ConfigParser()
    config.read('holeio.cfg')
    if config.get('oauth', 'token'):
        watcher.start_watching()
        downloader.start()

logging.debug("DEBUG logging visible")
logging.info("INFO logging visible")
logging.warning("WARNING logging visible")
db.create_tables()
db.add_history("Starting hole.io")
