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
from . import config
from . import ssh

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
        self.get_cluster_info(sub_cmd)
        self.azure.create_cluster(num=self.get_cluster_size())
        self.update_cluster_info(sub_cmd)

    def sshmaster(self, sub_cmd=None, **kwargs):
        try:
            cluster_name = sub_cmd[0]
        except:
            cluster_name = sub_cmd
        cluster_info = self.get_cluster_info(cluster_name)
        #SSH to cluster_info['master']
        sshmaster = SSH()
        sshmaster.setup(host=cluster_info['master'], pkey=cluster_info['pkey'])
        sshmaster.shell()

    def get_cluster_info(self, name=None):
        return self.get_conf(name)

    def set_cluster_info(self, name=None):
        data = {'master': None, \
                'engines': None, \
                'sshkey': None }
        config.set_cluster_conf(name, data)

    def update_cluster_info(self, name=None):
        engines = []
        for node_name, result in self.azure.results.iteritems():
            if node_name == "master":
                master = result
            else:
                engines.append(node_name)
        engines.remove(master)

        data = {'master': master, \
                'engines': engines, \
                'sshkey': None }
        config.set_cluster_conf(name, data)

    def get_conf(self, name):
        return config.get_cluster_conf(name)

    def get_cluster_size(self):
        '''Return a number of VM instances to deploy'''
        '''Temporarily returns 2'''
        return 2

    def _none(self, sub_cmd=None, **kwargs):
        return
