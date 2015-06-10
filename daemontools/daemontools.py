#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@script : daemontools.py
@about  :
"""
import os, re
import platform
from time import sleep, time
from utils import bash


class DaemontoolsError(Exception): pass


class Scanner:
  """ Simple svscan wrapper """
  def __init__(self):
    self.svscan_ = bash('ps ax |grep -Po "svscan\s+.*$"')[0].rstrip()
    self.svc_root_ = ''
    if (self.svscan_ != ''):
      self.svc_root_ = self.svscan_.split()[1]
    self.status_ = ''

  @classmethod
  def status(cls):
    return bash('status svscan', False)[0].rstrip()

  def running(self):
    self.status_ = self.status()
    return 'start/running' in self.status_

  def waiting(self):
    self.status_ = self.status()
    return 'stop/waiting' in self.status_

  def unknown(self):
    self.status_ = self.status()
    return 'Unknown job' in self.status_

  def start(self):
    if not self.running():
      ret = bash('start svscan', False)
      sleep(0.5)
    return self.running()

  def stop(self):
    if not self.waiting():
      ret = bash('stop svscan', False)
      sleep(0.5)
    return self.waiting()


class Daemontools:
  SVC_ROOT = '/etc/service'

  @classmethod
  def exists(cls, name):
    return cls._check_service_exists(name, False)

  @classmethod
  def status(cls, name):
    cls._check_service_exists(name)
    ret, err = system('svstat %s' % cls.path)
    if err: raise Exception(err)
    match = re.match('.*?:\s*(\S+).*\s(\d+) seconds.*', ret)
    if not match:
      raise DaemontoolsError('Unknown status')
    return (match.group(1), int(match.group(2)))

  @classmethod
  def up(cls, name):
    return cls.status(name)[0] == 'up'

  @classmethod
  def down(cls, name):
    return cls.status(name)[0] == 'down'

  @classmethod
  def start(cls, name):
    cls._run_service(name, 'u')

  @classmethod
  def stop(cls, name):
    cls._run_service(name, 'd')

  @classmethod
  def restart(cls, name):
    cls._run_service(name, 't')

  @classmethod
  def run_status(cls, name):
    cls._check_service_exists(name)
    if os.path.exists('%s/down' % cls.path): return 'down'
    else: return 'up'

  @classmethod
  def run_status_up(cls, name):
    return cls.run_status(name) == 'up'

  @classmethod
  def run_status_down(cls, name):
    return cls.run_status(name) == 'down'

  @classmethod
  def make_run_status_up(cls, name):
    cls._check_service_exists(name)
    os.unlink('%s/down' % cls.path)
    return True

  @classmethod
  def make_run_status_down(cls, name):
    cls._check_service_exists(name)
    with open('%s/down' % cls.path, 'w') as fd:
      fd.write('')
    return True

  @classmethod
  def list_services(cls):
    #return os.popen('ls -L %s' % cls.SVC_ROOT).read().rstrip().split('\n')
    result, lst = [], os.listdir(cls.SVC_ROOT)
    for name in lst:
      if os.path.isdir(os.path.join(cls.SVC_ROOT, name)):
        result.append(name)
    return result

  @classmethod
  def create(cls, name, script, log=None, down=False):
    path = os.path.join(cls.SVC_ROOT, name)
    run = os.path.join(path, 'run')
    #if os.path.isfile(run): return True

    if not os.path.isdir(path):
      subprocess.call(['mkdir', '-p', path])

    # init(current time) lasttime number for log monitoring
    with open(os.path.join(path, 'last_time'), 'w') as fd:
      fd.write( str(int(time())) )

    # create service
    if down:
      with open(os.path.join(path, 'down'), 'w') as fd: fd.write('')
    with open(run, 'w') as fd:
      fd.write(script)
    subprocess.call(['chmod', '+x', '%s' % run])

    if log is not None:
      subprocess.call(['mkdir', '-p', os.path.join(path, 'log')])
      log_run = os.path.join(path, 'log', 'run')
      with open(log_run, 'w') as fd:
        fd.write(log)
      subprocess.call(['chmod', '+x', '%s' % log_run])

    supervise = os.path.join(path, 'supervise')
    while 1:
      if os.path.isdir(supervise): break
      sleep(1)

    return True

  # private members
  @classmethod
  def _check_service_exists(cls, name, raise_error = True):
    cls.path = os.path.join(cls.SVC_ROOT, name)
    if raise_error:
      if not os.path.isdir(cls.path):
        raise DaemontoolsError('Service %s does not exists' % name)
    else:
      return os.path.isdir(cls.path)

  @classmethod
  def _run_service(cls, name, command):
    if platform.dist()[0].lower() == 'ubuntu':
      ret, err = system('status svscan')
      if 'stop' in ret: os.system('start svscan; sleep 1')
    cls._check_service_exists(name)
    ret, err = system('svc -%s %s' % (command, cls.path))
    if err: raise Exception(err)
    return True
