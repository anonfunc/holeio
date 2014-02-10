import os

import bottle
from bottle import route, get, post, view, request, redirect

import ConfigParser

from holeio import watcher, downloader
import logging
logger = logging.getLogger(__name__)

bottle.TEMPLATE_PATH.append(os.path.join(os.path.dirname(__file__), 'views'))

config = ConfigParser.ConfigParser()
config.read('holeio.cfg')

@get('/config')
@view('config')
def config():
  if not os.path.isfile("holeio.cfg"):
    return {"client_id": "",
            "client_secret": "",
            "token_set": False,
            "token": "",
            "host": "",
            "polling_interval": 5,
            "inactive_interval": 60,
            "blackhole_dir": "",
            "download_dir": ""}
  config = ConfigParser.RawConfigParser()
  config.read("holeio.cfg")
  host = config.get('web', 'host')
  client_id = config.get('oauth', 'client_id')
  client_secret = config.get('oauth', 'client_secret')
  token = config.get('oauth', 'token')
  blackhole_dir = config.get('directories', 'blackhole')
  download_dir = config.get('directories', 'download')
  polling_interval = config.get('intervals', 'polling')
  inactive_interval = config.get('intervals', 'inactive')
  return locals()

@post('/config')
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
  config.set('oauth', 'client_id', request.forms.client_id)
  config.set('oauth', 'token', request.forms.token)
  config.set('oauth', 'client_secret', request.forms.client_secret)
  config.set('directories', 'blackhole', request.forms.blackhole_dir)
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
  redirect("/config")

@get('/authorize')
@view('authorize')
def get_authorize():
  return dict()

@route('/')
@route('/history')
@view('history')
def history():
  return dict()
