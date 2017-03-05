# Hole.io
[![Stories in Ready](https://badge.waffle.io/anonfunc/holeio.png?label=ready)](http://waffle.io/anonfunc/holeio)

Hole.io is a "blackhole" downloader for [Put.io]("http://put.io") which does the following:
* Watches a "blackhole" directory for added torrent files
* Uploads the torrents to Put.io
* Watches the transfers for completion
* Downloads the completed files

Since I'm not dumb enough to intentionally check in my OAuth client secret for Put.io, you'll need to register an application to 
connect to Put.io.  See https://put.io/v2/docs/gettingstarted.html#sign-up and https://put.io/v2/oauth2/register.

You will be able to enter these into the configuration page to get connected.

## Category support

If you have subdirectories (one level deep) in the blackhole directory, they will be treated as "categories" and 
both Put.io transfers and the eventually downloaded files will be in subdirectories.

## Getting started (not very polished)

Clone this repo somewhere and set up a virtual environment:

    git clone https://github.com/anonfunc/holeio.git
    cd holeio
    ./install.sh
  
Start the server:

    nohup ./start.sh >> logfile &

Open 127.0.0.1:8080 (or whatever the IP address is of the host you are running on).

Click 'config' in the top, and fill in values:

* Username and password for admin
* Hostname
* Webroot for reverse proxying (leave blank if you want Hole.io to serve at /, must restart if changed) 
* OAuth configuration (See https://app.put.io/oauth/apps and https://put.io/v2/docs/gettingstarted.html#sign-up to get client ID and secret)
* Directories
* Polling intervals

After all that, you can add .torrent or .magnet files to Hole.io's blackhole directory.

## Put.io callback

You can also set the polling interval really high, and set a callback URL instead.
You'll need to make Hole.io somehow accessible to the internet, but after you have, that "Check for Finished Downloads" link can be pased into https://app.put.io/settings as the "Callback URL", causing Hole.io to check for finished downloads every time a download finishes.
