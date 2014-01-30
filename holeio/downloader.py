import threading
import ConfigParser
import time

from holeio import client

running = False
def loop():
  global running
  running = True
  while running:
    print "Looking for finished transfers"
    client.download_finished_transfers()
    config = ConfigParser.RawConfigParser()
    config.read("holeio.cfg")
    polling_interval = config.get('intervals', 'polling')
    time.sleep(int(polling_interval) * 60)

dl_thread = None
def start():
  global dl_thread
  dl_thread = threading.Thread(target=loop)
  dl_thread.daemon = True
  dl_thread.start()

def stop():
  global dl_thread
  global running
  if running:
    running = False
    print "Waiting for downloads to finish..."
    dl_thread.join()

def restart():
  stop()
  start()
