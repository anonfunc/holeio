import os
import ConfigParser

import putio

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
    return c.Transfer.add_torrent(torrent, dir.id, extract=True)
  except:
    print "Problem adding torrent"

def waiting_for_transfers():
  c = get_client()
  for transfer in c.Transfer.list():
    if transfer.downloaded:
      continue
    if transfer.status in ["COMPLETED", "SEEDING"]:
      continue
    parent_dir = transfer.save_parent_id
    grandparent_dir = 0
    if parent_dir != 0:
      grandparent_dir = c.File.get(parent_dir).parent_id
    holeio_id = ensure_directory("holeio").id
    if holeio_id in [parent_dir, grandparent_dir]:
      print "Found transfer under holeio dir."
      return True
  print "Did not find transfer under holeio dir."
  return False

def download_finished_transfers():
  c = get_client()
  config = ConfigParser.RawConfigParser()
  config.read("holeio.cfg")
  download_dir = config.get('directories', 'download')
  for transfer in c.Transfer.list():
    print "looking at transfer %s" % transfer
    print "status is %s" % transfer.status
    print "downloaded is %s" % transfer.downloaded
    if (transfer.status in ["COMPLETED", "SEEDING"]):
      print "Need to download finished transfer: %s" % transfer
      try:
        file = c.File.get(transfer.file_id)
      except Exception as e:
        print "Skipping file, %s" % e
        continue
      parent_dir = file.parent_id
      grandparent_dir = 0
      if parent_dir != 0:
        grandparent_dir = c.File.get(parent_dir).parent_id
      holeio_id = ensure_directory("holeio").id
      if holeio_id not in [parent_dir, grandparent_dir]:
        print "Not under holeio directory.  Skipping"
        continue

      if parent_dir != holeio_id and parent_dir != 0:
        # Use directory as a category
        category = c.File.get(parent_dir).name
      else:
        category = ""
      local_dir = os.path.join(download_dir, category)
      local_path = os.path.join(local_dir, file.name)
      if os.path.exists(local_path):
        print "Have %s already, skipping" % local_path
        continue
      if file.content_type == 'application/x-directory':
        # Mirror it locally
        os.makedirs(local_path)
      print "Starting download to %s..." % local_dir
      file.download(local_dir, delete_after_download=False)
      print "Finished."
