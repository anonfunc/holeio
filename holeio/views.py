import os

import bottle
from bottle import route, get, post, view, request, redirect, auth_basic

import ConfigParser

from holeio import watcher, downloader, db, client
import logging
logger = logging.getLogger(__name__)

bottle.TEMPLATE_PATH.append(os.path.join(os.path.dirname(__file__), 'views'))

config = ConfigParser.ConfigParser()
config.read('holeio.cfg')
try:
  WEBROOT = '/' + config.get('web', 'root').strip('/') + '/'
  WEBROOT.replace('//', '/')
except:
  WEBROOT = '/'


def check_user(user, password):
  global config
  expected_user = config.get('web', 'user')
  if not expected_user:
      return True
  if user != expected_user:
    return False
  if password != config.get('web', 'password'):
    return False
  return True


@get(WEBROOT + 'config')
@auth_basic(check_user)
@view('config')
def view_config():
  if not os.path.isfile("holeio.cfg"):
    return {"client_id": "",
            "client_secret": "",
            "token_set": False,
            "token": "",
            "host": "",
            "root": "",
            "user": "",
            "password": "",
            "polling_interval": 5,
            "inactive_interval": 60,
            "blackhole_dir": "",
            "incomplete_dir": "",
            "download_dir": ""}
  config = ConfigParser.RawConfigParser()
  config.read("holeio.cfg")
  host = config.get('web', 'host')
  root = config.get('web', 'root')
  user = config.get('web', 'user')
  password = config.get('web', 'password')
  client_id = config.get('oauth', 'client_id')
  client_secret = config.get('oauth', 'client_secret')
  token = config.get('oauth', 'token')
  blackhole_dir = config.get('directories', 'blackhole')
  incomplete_dir = config.get('directories', 'incomplete')
  download_dir = config.get('directories', 'download')
  polling_interval = config.get('intervals', 'polling')
  inactive_interval = config.get('intervals', 'inactive')
  return locals()

@post(WEBROOT + 'config')
@auth_basic(check_user)
def save_config():
  config = ConfigParser.RawConfigParser()
  if os.path.isfile("holeio.cfg"):
    config.read("holeio.cfg")
  else:
    config.add_section('web')
    config.add_section('oauth')
    config.add_section('directories')
    config.add_section('intervals')
  old_dir = ""
  if config.has_option("directories", "blackhole"):
    old_dir = config.get("directories", "blackhole")
  config.set('web', 'host', request.forms.host)
  config.set('web', 'root', request.forms.root)
  config.set('oauth', 'client_id', request.forms.client_id)
  config.set('oauth', 'token', request.forms.token)
  config.set('oauth', 'client_secret', request.forms.client_secret)
  config.set('directories', 'blackhole', request.forms.blackhole_dir)
  config.set('directories', 'incomplete', request.forms.incomplete_dir)
  config.set('directories', 'download', request.forms.download_dir)
  config.set('intervals', 'polling', request.forms.polling_interval)
  config.set('intervals', 'inactive', request.forms.inactive_interval)
  # Show the new config
  # Writing our configuration file to 'example.cfg'
  with open('holeio.cfg', 'wb') as configfile:
        config.write(configfile)
  if old_dir != request.forms.blackhole_dir:
    logger.info("New drop directory, restarting watcher")
    watcher.restart_watcher()
  downloader.start()
  redirect(WEBROOT + "config")

@get(WEBROOT + 'clearhistory')
@auth_basic(check_user)
def clear_history():
  db.clear_history()
  redirect(WEBROOT + "history")

@get(WEBROOT + 'wake')
@auth_basic(check_user)
def wake_downloader():
  downloader.wake()
  redirect(WEBROOT + "history")

@post(WEBROOT + 'wake')
def post_wake_downloader():
  downloader.wake()
  logger.info("Got POST to wake endpoint, content:")
  logger.info(request.forms)


@get(WEBROOT + 'authorize')
@auth_basic(check_user)
@view('authorize')
def get_authorize():
  return dict()

@route(WEBROOT)
@route(WEBROOT + 'history')
@auth_basic(check_user)
@view('history')
def history():
  return {'history': db.get_history()}


@post(WEBROOT + 'magnet')
@auth_basic(check_user)
def magnet():
  client.add_torrent_uri(request.forms.uri)
  redirect(WEBROOT + "history")
