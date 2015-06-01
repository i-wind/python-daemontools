"""
    python-daemontools
"""

__version__ = "0.0.2"
__url__     = "https://github.com/i-wind/python-daemontools"

from utils import system
from daemontools import Daemontools, DaemontoolsError
from remote import Remote, RemoteError
