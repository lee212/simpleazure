# -*- coding: utf-8 -*-

"""
simpleazure.template

This module supports writing/reading Azure Resourece Manager templates

 :copyright:
 :license: 

"""


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
