import os
from collections import defaultdict

import bottle
from bottle import route, get, post, view, request, redirect

import ConfigParser

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
            "host": "",
            "blackhole_dir": "",
            "download_dir": ""}
  config = ConfigParser.RawConfigParser()
  config.read("holeio.cfg")
  host = config.get('web', 'host')
  client_id = config.get('oauth', 'client_id')
  client_secret = config.get('oauth', 'client_secret')
  token_set = config.has_option('oauth', 'token')
  blackhole_dir = config.get('directories', 'blackhole')
  download_dir = config.get('directories', 'download')
  return locals()

@post('/set_token')
def set_token():
  config.set('oauth', 'token', request.forms.client_secret)
  config.add_section('directories')
  config.set('directories', 'blackhole', request.forms.blackhole_dir)
  config.set('directories', 'download', request.forms.download_dir)
  # Show the new config
  # Writing our configuration file to 'example.cfg'
  with open('holeio.cfg', 'wb') as configfile:
        config.write(configfile)
  redirect("/config")

@post('/config')
def save_config():
  config = ConfigParser.RawConfigParser()
  if os.path.isfile("holeio.cfg"):
    config.read("holeio.cfg")
  else:
    config.add_section('web')
    config.add_section('oauth')
    config.add_section('directories')

  config.set('web', 'host', request.forms.host)
  config.set('oauth', 'client_id', request.forms.client_id)
  config.set('oauth', 'client_secret', request.forms.client_secret)
  config.set('directories', 'blackhole', request.forms.blackhole_dir)
  config.set('directories', 'download', request.forms.download_dir)
  # Show the new config
  # Writing our configuration file to 'example.cfg'
  with open('holeio.cfg', 'wb') as configfile:
        config.write(configfile)
  redirect("/config")

@route('/')
@route('/history')
@view('history')
def history():
  return dict()
