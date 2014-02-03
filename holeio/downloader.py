import threading
import ConfigParser

from holeio import client

running = False
wakeup = threading.Condition()

def loop():
  global running
  running = True
  while running:
    print "Looking for finished transfers"
    client.download_finished_transfers()
    config = ConfigParser.RawConfigParser()
    config.read("holeio.cfg")
    polling_interval = config.get('intervals', 'polling')
    inactive_interval = config.get('intervals', 'inactive')
    wakeup.acquire()
    if client.waiting_for_transfers():
      print "Still have transfers, short poll."
      wakeup.wait(int(polling_interval) * 60)
    else:
      print "No transfers, long poll"
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
    print "Started downloader"

def stop():
  global dl_thread
  global running
  if running:
    running = False
    print "Waiting for downloads to finish..."
    dl_thread.join()

def wake():
  wakeup.acquire()
  wakeup.notify()
  print "Waking Downloader..."
  wakeup.release()
