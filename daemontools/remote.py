#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@script : remote.py
@about  :
"""

from utils import system

class RemoteError(Exception): pass

class Remote:
  def __init__(self, server):
    self.server = server
    self.svc_root = '/etc/service'
    self.log_root = '/var/log/svc'
    self.path = ''

  def list_svc(self):
    ret, err = system('ssh webcaster@%s sudo svstat %s/* 2>&1' % (self.server, self.svc_root))
    if err: raise RemoteError(err)
    return [line for line in ret.split('\n') if line]

  def get_scripts(self, service):
    cmd = 'ssh webcaster@%s cat %s/run' % (self.server, service)
    gen_log.info( cmd )
    run = system( cmd )[0]
    cmd = 'ssh webcaster@%s cat %s/log/run' % (self.server, service)
    gen_log.info( cmd )
    log = system( cmd )[0]
    return (run, log)

  def stop(self, name):
    self._run_svc(name, 'd')

  def start(self, name):
    self._run_svc(name, 'u')

  def restart(self, name):
    self._run_svc(name, 't')

  # private members
  def _check_service_exists(self, name, raise_error = True):
    self.path = '%s/%s' % (self.svc_root, name)
    ret = os.popen('ssh webcaster@%s [ -d %s ] && echo 1 || echo 0' % (self.server, self.path)).read()
    if raise_error:
      if ret=='0':
        raise RemoteError('Service %s does not exists' % name)
    else:
      return ret=='1'

  def _run_svc(self, name, command):
    self._check_service_exists(name)
    ret, err = system('ssh webcaster@%s sudo svc -%s %s 2>&1' % (self.server, command, self.path))
    if err: raise RemoteError(err)
    return True
