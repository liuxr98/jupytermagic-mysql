from __future__ import absolute_import
from .mysqlmagic import MySQLMagic


def load_ipython_extension(ipython):
    mymagic = MySQLMagic(ipython)    
    ipython.register_magics(mymagic)