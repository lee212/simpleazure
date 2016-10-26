# -*- coding: utf-8 -*-

"""
simpleazure.template.reader

This module supports reading contents from json files to compile templates

 :copyright:
 :license: 

"""

import json
import os
import urllib
from urlparse import urlparse
from pprint import pprint
from .template import Template

class Reader(object):
    """Constructs a :class:`Reader <Reader>`.
    Returns :class:`Reader <Reader>` instance.

    Usage::

    """

    default_dir = os.path.dirname(os.path.realpath(__file__)) + "/defaults/" 
    template = Template()

    def __init__(self, path_or_uri=None):
        if path_or_uri:
            self.read_template(path_or_uri)

    def read_template(self, path_or_uri):

        if urlparse(path_or_uri).scheme is not "":
            template = json.loads(urllib.urlopen(path_or_uri).read())
        else:
            with open(path_or_uri, "r") as temp:
                template = json.loads(temp.read())
        self.template = Template(template)

    def get_defaults(self):
        return self.read_defaults()

    def read_defaults(self):

        path = self.default_dir
        files = [ f for f in os.listdir(path) if
                os.path.isfile(os.path.join(path, f))]
        # and os.path.splitext(f)[1] == '.json'] 
        template = {}
        for filename in files:
            name = os.path.splitext(filename)[0] 
            ext = os.path.splitext(filename)[1]
            with open(path + filename, "r") as f:
                template[name] = json.loads(f.read())

        self.template = template
        return template

    def show(self, section=None):
        if section:
            pprint(self.template[section])
        else:
            pprint(self.template)

