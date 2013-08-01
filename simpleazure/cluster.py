# -*- coding: utf-8 -*-

"""
simpleazure.cluster
~~~~~~~~~~~~~~~~~~~~~~~~

This module provides a Python library for Windows Azure Virtual Machines.

 :copyright: TBD
 :license: TBD

"""
import sys
from simpleazure import SimpleAzure

class Cluster(object):
    def __init__(self):
        return
    
    def cli(self, args=None, opts=None, **kwargs):
        self.args = args
        self.opts = opts
        self.kwargs = kwargs

        try:
            main_cmd = self.args[0]
            sub_cmd = self.args[1:]
            func = getattr(self, main_cmd)
            func(sub_cmd)
        except:
            print sys.exc_info()
            pass

    def start(self, sub_cmd=None, **kwargs):
        return
