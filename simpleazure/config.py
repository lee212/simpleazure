# -*- coding: utf-8 -*-

"""
config.Config
~~~~~~~~~~~~~~~~~~~~~~~~

This module provides a Python library for Windows Azure Virtual Machines.

 :copyright: TBD
 :license: TBD

"""
import os

DEFAULT_AZURE_CONFIG_PATH = os.environ["HOME"] + '/.azure'

def config_path():
    return DEFAULT_AZURE_CONFIG_PATH
