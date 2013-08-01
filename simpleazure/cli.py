# -*- coding: utf-8 -*-

"""
simpleazure.CLI
~~~~~~~~~~~~~~~~~~~~~~~~

This module provides a Python library for Windows Azure Virtual Machines.

 :copyright: TBD
 :license: TBD

"""
import optparse
from . import cluster

class CLI:

    def __init__(self, name=None):
        self.module_name = name

    def get_parameter(self):
        parser = optparse.OptionParser()
        (self.callopts, self.callargs) = parser.parse_args()

    def execute(self):
        if self.module_name == "cluster":
            a = cluster.Cluster()
            a.cli(args=self.callargs, opts=self.callopts)

    def main(self):
        self.get_parameter()
        self.execute()
