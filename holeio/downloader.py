import threading
import ConfigParser

from holeio import client, db
import logging
logger = logging.getLogger(__name__)

running = False
wakeup = threading.Condition()

def loop():
  global running
  running = True
  while running:
    logger.info("Looking for finished transfers")
    try:
      client.download_finished_transfers()
    except:
      logger.exception('Exception while downloading')
    config = ConfigParser.RawConfigParser()
    config.read("holeio.cfg")
    polling_interval = config.get('intervals', 'polling')
    inactive_interval = config.get('intervals', 'inactive')
    wakeup.acquire()
    if client.waiting_for_transfers():
      logger.info("Still have transfers, short poll. Waiting for %s minutes" %
                  polling_interval)
      wakeup.wait(int(polling_interval) * 60)
    else:
      logger.info("No transfers, long poll, waiting for %s minutes " %
                  inactive_interval)
      wakeup.wait(int(inactive_interval) * 60)
    wakeup.release()

dl_thread = None
def start():
  global dl_thread
  global running
  if not dl_thread and not running:
    dl_thread = threading.Thread(target=loop)
    dl_thread.daemon = True
    dl_thread.start()
    logger.info("Started downloader")

def stop():
  global dl_thread
  global running
  if running:
    running = False
    logger.info("Waiting for downloads to finish...")
    dl_thread.join()

def wake():
  wakeup.acquire()
  wakeup.notify()
  logger.info("Waking Downloader...")
  db.add_history("Woke downloader")
  wakeup.release()
