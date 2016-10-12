# -*- coding: utf-8 -*-

"""
simpleazure.template

This module supports writing/reading Azure Resourece Manager templates

 :copyright:
 :license: 

"""
import pandas as pd

class Template(dict):

    azuredeploy = parameters = metadata = nested = scripts = etc = None
    special_placeholders = [ 'GEN-UNIQUE', 'GEN-UNIQUE-', 'GEN-SSH-PUB-KEY', 'GEN-PASSWORD' ]

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
                new[f['type']] = f['dependsOn']
            except:
                new[f['type']] = ""

        return pd.Series(new)

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
