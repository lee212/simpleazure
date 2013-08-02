# -*- coding: utf-8 -*-

"""
utils
~~~~~~~~~~~~~~~~~~~~~~~~

This module provides a Python library for Windows Azure Virtual Machines.

 :copyright: TBD
 :license: TBD

"""

import os

def ensure_dir_exists(directory):
    try:
        if not os.path.exists(directory):
                os.makedirs(directory)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
           raise
