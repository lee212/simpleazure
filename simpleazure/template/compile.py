# -*- coding: utf-8 -*-

"""
simpleazure.template.compile

This module compiles Azure Resource Manager Templates

 :copyright:
 :license: 

"""

from reader import Reader
from template import Template

class Compile(object):
    """Constructs a :class:`Compile <NEW>`.
    Returns :class:`Compile <NEW>` instance.

    Usage::

    """

    def __init__(self):
        self.template = Template()
        self.reader = Reader()


def main():
    template_deployment = Compile()
    temp = template_deployment.reader.get_defaults()
    asvm = temp['azuredeploy']
    # read arm class
    # set parameter
