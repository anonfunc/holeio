import os
import ConfigParser
import shutil

import putiopy
import logging

from holeio import db

logger = logging.getLogger(__name__)
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
    if token:
        client = putiopy.Client(token)
        return client
    logger.error('No oauth token set')


def ensure_directory(name, parent=0):
    client = get_client()
    root_dirs = [file.name for file in client.File.list(parent)]
    if name not in root_dirs:
        client.request("/files/create-folder", method="POST",
                       data={"name": name, "parent_id": parent})
    dir_obj = [file for file in client.File.list(parent) if file.name == name][0]
    return dir_obj


def add_torrent_uri(torrent_uri, category=None):
    try:
        c = get_client()
        dir = ensure_directory("holeio")
        # Transfer object
        if category:
            dir = ensure_directory(category, dir.id)
        # Bugged: Doesn't pass parent.
        # result = c.Transfer.add_url(torrent_uri, dir.id, extract=True)
        # result = c.Transfer.add_url(torrent_uri, dir.id, extract=True)
        c.request("/transfers/add", method="POST",
                  data={"url": torrent_uri,
                        "save_parent_id": dir.id,
                        "extract": True})
        db.add_history("Added magnet link %s" % str(torrent_uri))
        # return result
        return True
    except:
        logger.error("Problem adding torrent")
        db.add_history("Problem adding torrent %s" % str(torrent_uri))


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
    incomplete_dir = config.get('directories', 'incomplete')
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
            local_dir = os.path.join(incomplete_dir, category)
            finished_dir = os.path.join(download_dir, category)
            local_path = os.path.join(local_dir, file.name)
            finished_path = os.path.join(finished_dir, file.name)
            if os.path.exists(local_path):
                logger.info("%s exists, deleting and trying over")
                shutil.rmtree(local_path)
            if file.content_type == 'application/x-directory':
                # Mirror it locally
                if not os.path.exists(local_dir):
                    try:
                        os.makedirs(local_dir)
                    except OSError:
                        pass
            logger.info("Starting download to %s..." % local_path)
            db.add_history("Starting download to %s" % local_path)
            file.download(local_dir, delete_after_download=True)
            logger.info("Finished downloading file to %s. Changing permissions.",
                        local_path)
            db.add_history("Finished download to %s. Changing permissions" %
                           local_path)
            if os.path.isdir(local_path):
                os.chmod(local_path, 0o777)
                for root, dirs, files in os.walk(local_path):
                    for d in dirs:
                        os.chmod(os.path.join(root, d), 0o777)
                    for f in files:
                        os.chmod(os.path.join(root, f), 0o666)
            try:
                os.makedirs(finished_dir)
            except OSError:
                pass
            os.rename(local_path, finished_path)
            logger.info("Renamed from %s to %s", local_path, finished_path)
            db.add_history("Renamed from %s to %s" % (local_path, finished_path))
    for transfer in c.Transfer.list():
        print transfer.name, transfer.status
        if transfer.status in ['DOWNLOADING', 'IN_QUEUE']:
            continue
        if transfer.is_private:
            # TODO: configurable ratio
            if transfer.status == 'SEEDING' or transfer.current_ratio < 1.99:
                continue
        print 'Removing transfer %s' % transfer.name
        transfer.cancel()
