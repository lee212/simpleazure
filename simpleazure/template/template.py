# -*- coding: utf-8 -*-

"""
simpleazure.template

This module supports writing/reading Azure Resourece Manager templates

 :copyright:
 :license: 

"""

#TODO: replace pandas data series. data frame with simple functions
#
        
from pprint import pprint
import pandas as pd
from collections import OrderedDict, defaultdict
from itertools import islice, izip_longest

class Templates(OrderedDict):
    _list = None
    _list_page = 0
    _list_inc = 10

    def get_sorted_by_key(self):
        new = Templates(sorted(self.items()))
        return new

    def ten(self):
        self._list_inc = 10
        return self.page()

    def twenty(self):
        self._list_inc = 20
        return self.page()

    def page(self):
        if not self._list:
            self._list = list(grouper(self, self._list_inc))
        res = {}

        try:
            self._list[self._list_page]
        except IndexError as e:
            print ("= last page! =")
            self._list_page -= 1

        for name in self._list[self._list_page]:
            try:
                res[name] = self[name].metadata().itemDisplayName
            # if metadata is not available
            except Exception as e:
                res[name] = ""
        if len(self._list) > self._list_page:
            self._list_page += 1
        return pd.Series(res)

    def next(self):
        return self.page()

    def first(self):
        self._list_page = 0
        return self.page()

# from https://docs.python.org/2/library/itertools.html
def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)

def tree(): return defaultdict(tree)
def dicts(t): return {k: dicts(t[k]) for k in t}
def depth(d, level=1):
    if not isinstance(d, dict) or not d:
        return level
    return max(depth(d[k], level + 1) for k in d)

class Template(dict):

    azuredeploy = parameters = metadata = nested = scripts = etc = None
    special_placeholders = [ 'GEN-UNIQUE', 'GEN-UNIQUE-', 'GEN-SSH-PUB-KEY', 'GEN-PASSWORD' ]
    dependency = None

    def metadata(self):
        return pd.Series(self['metadata'])

    def parameters(self):
        #return pd.Series(self['parameters']['parameters'])
        return pd.Series(self._key_and_value(self['parameters']['parameters']))

    def variables(self):
        return pd.Series(self['azuredeploy']['variables'])

    def outputs(self):
        try:
            return pd.Series(self._key_and_value(self['azuredeploy']['outputs']))
            #return pd.Series(self['azuredeploy']['outputs'])
        except:
            return 

    def resources(self):
        new = {}
        for f in self['azuredeploy']['resources']:
            try:
                new[f['type']] = f
            except:
                new[f['type']] = ""

        return pd.Series(new)

    def dependson(self):
        new = tree()
        for resource in self['azuredeploy']['resources']:
            try:
                if 'dependsOn' in resource:
                    for depend in resource['dependsOn']:
                        depend_typename = self._get_typename(depend)
                        val = self._lookup(depend_typename)
                        new[resource['type']][depend_typename] = val
            except:
                new[resource['type']] = self._run_template_functions(resource['name'])

        depth_cnt = 0
        pick_one = None
        for k,v in new.iteritems():
            depth_k = depth(v)
            if depth_k > depth_cnt:
                pick_one = k
                depth_cnt = depth_k

        temp = tree()
        temp[pick_one] = new[pick_one]
        self.dependency = dicts(temp)
        return dicts(temp)

    def dependson_print(self):
        pprint(self.dependency)

    def _run_template_functions(self, value):
        concat = self._concat
        variables = self._variables
        try:
            return eval(value)[0]
        except Exception as e:
            return value

    def _get_typename(self, value):
        try:
            result = self._run_template_functions(value).split("/")
            return "/".join(result[0:2])
        except Exception as e:
            return value

    def _lookup(self, typename):
        new = tree()
        try:
            for resource in self['azuredeploy']['resources']:
                if typename == resource['type']:
                    if 'dependsOn' in resource:
                        for depend in resource['dependsOn']:
                            depend_typename = self._get_typename(depend)
                            val = self._lookup(depend_typename)
                            new[depend_typename] = val
                    else:
                        val = self._run_template_functions(resource['name'])
                        new[val] = {}
                    return new
        except:
            return new

    # Azure Template function
    def _concat(self, *args):
        strings = ""
        for arg in args:
            strings += arg
        return strings

    # Azure Template function
    def _variables(self, name):
        try:
            var = self['azuredeploy']['variables'][name]
        except:
            var = name
        try:
            return eval(var)
        except:
            return var

    def requirements(self):
        required = {}

        for k, v in self['parameters']['parameters'].iteritems():
            try:
                if v['value'][:4] == "GEN-":
                    required[k] = v['value']
            except:
                pass
        return required

    def summary(self):
        (required, others) = self._get_parameters()
        # name, count, values
        return [
                [len(required) + ' Required parameters', ', '.join(required)],
                [len(self['azuredeploy']['resources']) + ' Resources', ', '.join([ f['type'] for f in self['azuredeploy']['resources'] ])],
                ]

    def _get_parameters(self):
        required = []
        others = []
        for k, v in self['parameters']['parameters'].iteritems():
            try:
                if v['value'][:4] == "GEN-":
                    required.append(k + "(" + v['value'] + ")")
                else:
                    others.append(k + "(" + v['value'] + ")")
            except:
                others.append(k + "(" + v['value'] + ")")
        return (required, others)

    def _get_resources(self):
        #for k,v in self['azuredeploy']['resources'].iter
        pass

    def _key_and_value(self, dict_with_value):
        new_dict = {}
        try:
            for k, v in dict_with_value.iteritems():
                new_dict[k] = v['value']
        except:
            pass
        return new_dict

class Deploy(object):
    """Constructs a :class:`Deploy <Deploy>`.
    Returns :class:`Deploy <Deploy>` instance.

    """

    contentVersion = ""
    parameters = {}
    variables = {}
    resources = []
    outputs = {}
    __struct__ = {
            "$schema": "http://schema.management.azure.com/schemas/2015-01-01/deploymentTemplate.json#",
            "contentVersion": "",
            "parameters": {  },
            "variables": {  },
            "resources": [  ],
            "outputs": {  }
            }

class Parameters(object):
    """Constructs a :class:`Parameters <Parameters>`.
    Returns :class:`Parameters <Parameters>` instance.

    """

    contentVersion = ""
    parameters = {}

    parameter = { 
            "name": {
                "type": "",
                "defaultValue": 0,
                "metadata": { "description": "" },
                "minValue":0,
                "maxValue":0,
                "allowedValues": []

        } 
    }

    __struct__ = {
            "$schema": "http://schema.management.azure.com/schemas/2015-01-01/deploymentParameters.json#",
            "contentVersion": "1.0.0.0",
            "parameters": {
                }
            }

class Metadata(object):
    """Constructs a :class:`Metadata <Metadata>`.
    Returns :class:`Metadata <Metadata>` instance.

    """
    itemDeplayName = ""
    description = ""
    summary = ""
    githubUsername = ""
    dateUpdated = ""

    __struct__ = {
        "itemDisplayName": "Blank Template",
        "description": "A blank template and empty parameters file.",
        "summary": "A blank template and empty parameters file.  Use this template as the framework for your custom deployment.",
        "githubUsername": "",
        "dateUpdated": "2016-09-28"
        }

# Tips
# See blank template from 
# https://github.com/Azure/azure-quickstart-templates/blob/master/100-blank-template/metadata.json

# Document
# https://azure.microsoft.com/en-us/documentation/articles/resource-group-authoring-templates/
