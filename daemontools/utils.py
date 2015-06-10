#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@script : utils.py
@about  :
"""
import shlex
import subprocess

def system(command):
  """
  System command execution result
  $ ret=system('dmesg | grep hda')
  $ print ret[0]
  """
  if isinstance(command, basestring):
    if '|' in command:
      cmd_list = (shlex.split(c) for c in command.strip().split('|'))
      prev = None
      for cmd in cmd_list:
        p = subprocess.Popen(cmd,
                 stdin =prev.stdout if prev else None,
                 stdout=subprocess.PIPE,
                 stderr=subprocess.PIPE)
        if prev: prev.stdout.close()
        prev = p
      return p.communicate()
    else:
      cmd = command.split()
  else:
    cmd = command

  p = subprocess.Popen(cmd,
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)
  # communicate возвращает tuple (stdout, stderr)
  return p.communicate()


def bash(command, shell=True):
  """
  System command execution result
  $ ret=bash('dmesg | grep hda')
  $ print ret[0]
  """
  if shell:
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
  else:
    p = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  return p.communicate()
