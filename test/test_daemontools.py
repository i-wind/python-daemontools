#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys
import unittest

sys.path.insert(0, '..')

import daemontools as dt

class SystemTests(unittest.TestCase):
  def test_system(self):
    self.assertEqual('__version__ = "0.0.1"\n', dt.system('cat ../daemontools.py |grep version')[0])

  def test_system_ls(self):
    self.assertEqual('test_daemontools.py\n', dt.system('ls')[0])


if __name__ == '__main__':
  unittest.main(verbosity = 2)
