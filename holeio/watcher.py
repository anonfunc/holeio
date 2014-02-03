import os
import time
import ConfigParser

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from holeio import client
from holeio import downloader

class TorrentEventHandler(FileSystemEventHandler):
  def __init__(self, token):
    super(TorrentEventHandler, self).__init__()
    self.token = token

  def check_file(self, file_path):
    if not file_path.endswith(".torrent"):
      print "%s not a torrent" % file_path
      return

    # Sanity check: starts with download dir
    config = ConfigParser.ConfigParser()
    config.read('holeio.cfg')
    blackhole_dir = config.get('directories', 'blackhole')
    if not file_path.startswith(blackhole_dir):
      print "Not sure how we got this event..."
      return
    relpath = os.path.relpath(file_path, blackhole_dir)
    category = os.path.dirname(relpath)
    print "I think it's in category %s" % category
    client.add_torrent(file_path, category)
    os.rename(file_path, file_path + ".added")
    print "Let's wake up the downloader, if needed"
    downloader.wake()

  def on_created(self, event):
    self.check_file(event.src_path)

  def on_moved(self, event):
    self.check_file(event.dest_path)

observer = None

def start_watching():
  global observer
  config = ConfigParser.ConfigParser()
  config.read('holeio.cfg')
  token = config.get('oauth', 'token')
  blackhole_dir = config.get('directories', 'blackhole')
  event_handler = TorrentEventHandler(token)
  if observer is None:
    observer = Observer()
    observer.schedule(event_handler, path=blackhole_dir, recursive=True)
  observer.start()
  print "Started watching %s " % blackhole_dir

def stop_watching():
  global observer
  if observer is not None:
    observer.stop()
    if observer.is_alive():
      observer.join()
    observer = None
    print "Stopped watching"

def restart_watcher():
  stop_watching()
  start_watching()
