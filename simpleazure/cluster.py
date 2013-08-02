# -*- coding: utf-8 -*-

"""
simpleazure.cluster
~~~~~~~~~~~~~~~~~~~~~~~~

This module provides a Python library for Windows Azure Virtual Machines.

 :copyright: TBD
 :license: TBD

"""
import sys
from simpleazure import SimpleAzure as saz

class Cluster(object):

    def __init__(self):

        # Virtual Machines
        self.azure = saz()
        self.azure.get_config()

        # cluster info
        
    
    def cli(self, args=None, opts=None, **kwargs):
        self.args = args
        self.opts = opts
        self.kwargs = kwargs

        try:
            main_cmd = self.args[0]
            sub_cmd = self.args[1:]
        except:
            main_cmd = '_none'
            sub_cmd = None
            pass

        func = getattr(self, main_cmd)
        func(sub_cmd)

    def start(self, sub_cmd=None, **kwargs):
        self.azure.create_vm()

    def sshmaster(self, sub_cmd=None, **kwargs):
        self.get_selected_cluster(sub_cmd)
        return

    def get_selected_cluster(self, name=None):
        self.get_info()

    def get_info(self):



    def _none(self, sub_cmd=None, **kwargs):
        return
