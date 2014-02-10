import os
import ConfigParser

import putio
import logging
logger = logging.getLogger(__name__)

from holeio import db

client = None
def get_client():
  global client
  if not os.path.isfile("holeio.cfg"):
    return None
  if client:
    return client
  config = ConfigParser.RawConfigParser()
  config.read("holeio.cfg")
  token = config.get('oauth', 'token')
  client = putio.Client(token)
  return client

def ensure_directory(name, parent=0):
  client = get_client()
  root_dirs = [file.name for file in client.File.list(parent)]
  if name not in root_dirs:
    client.request("/files/create-folder", method="POST",
                   data={"name": name, "parent_id": parent})
  dir_obj = [file for file in client.File.list(parent) if file.name == name][0]
  return dir_obj

def add_torrent(torrent, category=None):
  try:
    c = get_client()
    dir = ensure_directory("holeio")
    # Transfer object
    if category:
      dir = ensure_directory(category, dir.id)
    result = c.Transfer.add_torrent(torrent, dir.id, extract=True)
    db.add_history("Uploaded torrent from %s" % str(torrent))
    return result
  except:
    logger.error("Problem adding torrent")
    db.add_history("Problem uploading torrent from %s" % str(torrent))

def waiting_for_transfers():
  c = get_client()
  for transfer in c.Transfer.list():
    parent_dir = transfer.save_parent_id
    grandparent_dir = 0
    if parent_dir != 0:
      grandparent_dir = c.File.get(parent_dir).parent_id
    holeio_id = ensure_directory("holeio").id
    if holeio_id in [parent_dir, grandparent_dir]:
      logger.info("Found transfer under holeio dir.")
      return True
  logger.info("Did not find transfer under holeio dir.")
  return False

def download_finished_transfers():
  c = get_client()
  config = ConfigParser.RawConfigParser()
  config.read("holeio.cfg")
  download_dir = config.get('directories', 'download')
  for transfer in c.Transfer.list():
    logger.info("looking at transfer %s" % transfer)
    logger.info("status is %s" % transfer.status)
    logger.info("downloaded is %s" % transfer.downloaded)
    if (transfer.status in ["COMPLETED", "SEEDING"]):
      logger.info("Need to download finished transfer: %s" % transfer)
      try:
        file = c.File.get(transfer.file_id)
      except Exception as e:
        logger.info("Skipping file, %s" % e)
        continue
      parent_dir = file.parent_id
      grandparent_dir = 0
      if parent_dir != 0:
        grandparent_dir = c.File.get(parent_dir).parent_id
      holeio_id = ensure_directory("holeio").id
      if holeio_id not in [parent_dir, grandparent_dir]:
        logger.info("Not under holeio directory.  Skipping")
        continue

      if parent_dir != holeio_id and parent_dir != 0:
        # Use directory as a category
        category = c.File.get(parent_dir).name
      else:
        category = ""
      local_dir = os.path.join(download_dir, category)
      local_path = os.path.join(local_dir, file.name)
      if os.path.exists(local_path):
        logger.info("Have %s already, skipping" % local_path)
        continue
      if file.content_type == 'application/x-directory':
        # Mirror it locally
        os.makedirs(local_path)
      logger.info("Starting download to %s..." % local_dir)
      db.add_history("Starting download to %s" % local_path)
      file.download(local_dir, delete_after_download=True)
      logger.info("Finished downloading file to %s.", local_path)
      db.add_history("Finished download to %s" % local_path)
  logger.info("Done with all transfers, cleaning.")
  c.Transfer.clean()

