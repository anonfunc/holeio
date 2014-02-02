from fabric.api import local, run, env, cd, put
import os

env.hosts = ['nas']
env.port = 22
env.user = 'jdoe'
env.shell = '/bin/sh -c'

code_dir = "/volume1/homes/%s/code/holeio" & env.user

def host_type():
  run('uname -s')

#def prepare_deploy():
  #local("git add -p && git commit")
  #local("git push")

def kill():
  with cd(code_dir):
    run("test -f holeio.pid && kill $(<holeio.pid) || true")

def start():
  with cd(code_dir):
    run("./start.sh")

def push():
  run("mkdir -p %s" % code_dir)
  # Synology translates the SFTP paths into /share name/, not /volume1/share name/
  # Also, home is special.  Goes to /volume1/homes/user
  put("*.py", "/home/code/holeio/")
  put("*.txt", "/home/code/holeio/")
  put("*.sh", "/home/code/holeio/")
  if os.path.isfile("holeio.cfg"):
    put("holeio.cfg", "/home/code/holeio/")
  put("holeio/", "/home/code/holeio/")

def deploy():
  kill()
  push()
  start()
