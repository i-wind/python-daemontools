import re
from setuptools import setup

_version_re = re.compile(r'__version__\s+=\s+\"(.*)\"')

with open('daemontools.py', 'rb') as f:
    f = f.read()
    version = _version_re.search(f.decode('utf-8')).group(1)

setup(
  name = 'daemontools',
  version = version,
  py_modules = ["daemontools"],
  description = "Tools for communicating with daemontools supervisors.",
  long_description = open('README.rst').read(),
  author = 'Igor A. Vetrov',
  author_email = 'ig-wind@mail.ru',
  license = 'MIT',
  keywords = 'daemontools',
  url = 'https://github.com/i-wind/python-daemontools',
  download_url = 'https://github.com/i-wind/python-daemontools/archive/v%s.tar.gz' % version,
  classifiers = [
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.7",
    ("Topic :: Software Development :: Libraries :: Python Modules"),
  ],
)
