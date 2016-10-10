# -*- coding: utf-8 -*-

"""
simpleazure.azure-quickstart-templates

This module supports listing all azure-quickstart-templates from github

 :copyright:
 :license: 

"""

from github_api import GithubAPI
from github_cli import GithubCLI
import json
import inspect
import os.path
import collections

class AzureQuickStartTemplates(object):
    """Constructs a :class:`AzureQuickStartTemplates <AzureQuickStartTemplates>`.
    Returns :class:`AzureQuickStartTemplates <AzureQuickStartTemplates>` instance.

    Description:
    Azure provides a list of ARM templates written by community developers and
    this class reads the list and downloads json data to run the template directly.

    """
    api_or_cli = 'cli' #CLI uses git clone to read contents instead of API

    def __init__(self, mode="cli"):
        
        self.api_or_cli = mode

        self.api = GithubAPI()
        self.git_repo = "azure-quickstart-templates"
        self.git_owner = "Azure"
        self.git_clone = 'https://github.com/Azure/azure-quickstart-templates.git'

        if mode == "cli":
            self.cli = GithubCLI(self.git_clone)

    def get_list(self):
        """Returns a list of items in a repository except files"""
        my_func_name = inspect.stack()[0][3]
        func = getattr(self, my_func_name + "_" + self.api_or_cli)
        return func()

    def get_list_cli(self):
        res = collections.OrderedDict()
        items = self.cli.get_list()
        for item in items:
            if item == ".github":
                continue
            if item == "1-CONTRIBUTION-GUIDE":
                continue

            try:
                # requred
                azuredeploy = self.get_azuredeploy_cli(item)
                parameters = self.get_parameters_cli(item)
                meta = self.get_metadata_cli(item)
            except:
                continue
            etc = self.get_all_cli(item)
            nested = self.get_nested_cli(item)
            scripts = self.get_scripts_cli(item)
            res[item] = { 
                    "azuredeploy": azuredeploy,
                    "parameters": parameters,
                    "metadata": meta,
                    "nested": nested,
                    "scripts": scripts,
                    "etc": etc
                    }
            meta = azuredeploy = parameters = nested = scripts = etc = ""
        return res

    def get_list_api(self):

        self.api.set_var("repo", self.git_repo)
        self.api.set_var("owner", self.git_owner)
        #res = [ item if item['type'] == "dir" for item in self.api.get_list() ]
        res = collections.OrderedDict()

        items = self.api.get_list()
        for item in items:
            if item['type'] != "dir":
                continue
            if item['name'] == ".github":
                continue
            if item['name'] == "1-CONTRIBUTION-GUIDE":
                continue
            try:
                # required files
                azuredeploy = self.get_azuredeploy_api(item['path'])
                parameters = self.get_parameters_api(item['path'])
                meta = self.get_metadata_api(item['path'])
            except:
                # If fails, skip to next
                continue
            etc = self.get_all_api(item['path'])
            nested = self.get_nested_api(item['path'])
            scripts = self.get_scripts_api(item['path'])
            res[item['name']] = { 
                    "azuredeploy": azuredeploy,
                    "parameters": parameters,
                    "metadata": meta,
                    "nested": nested,
                    "scripts": scripts,
                    "etc": etc
                    }
            meta = azuredeploy = parameters = nested = scripts = etc = ""
        return res

    def get_metadata_api(self, path):
        """Returns cotents of the metadata.json file from a path"""
        self.api.set_var("path", path + "/metadata.json")
        return self._get_json_contents(self.api.get_file())

    def get_azuredeploy_api(self, path):
        """Returns cotents of the azuredeploy.json file from a path"""
        self.api.set_var("path", path + "/azuredeploy.json")
        return self._get_json_contents(self.api.get_file())

    def get_parameters_api(self, path):
        """Returns cotents of the azuredeploy.parameters.json file from a path"""
        self.api.set_var("path", path + "/azuredeploy.parameters.json")
        return self._get_json_contents(self.api.get_file())

    def get_nested_api(self, path):
        """Returns nested templates from a path"""
        self.api.set_var("path", path + "/nested")
        return self.api.get_list() or ""

    def get_scripts_api(self, path):
        """Returns scripts from a path"""
        self.api.set_var("path", path + "/scripts")
        return self.api.get_list() or ""

    def get_all_api(self, path):
        """Returns all items from a path"""
        self.api.set_var("path", path)
        return self.api.get_list() 

    def _get_json_contents(self, content):
        try:
            data = json.loads(content)
        except Exception as e:
            #TODO 
            # Some json data could not be decoded
            # e.g. /azure-quickstart-templates/201-logic-app-veter-pipeline/azuredeploy.json
            #print ("Failed to read json, {0}".format (e))
            data = content
        return data

    def get_metadata_cli(self, path):
        content = self.cli.get_file(os.path.join(path, "metadata.json"))
        print (path)
        return self._get_json_contents(content)

    def get_azuredeploy_cli(self, path):
        content = self.cli.get_file(os.path.join(path, "azuredeploy.json"))
        print (path)
        return self._get_json_contents(content)

    def get_parameters_cli(self, path):
        content = self.cli.get_file(os.path.join(path, "azuredeploy.parameters.json"))
        print (path)
        return self._get_json_contents(content)

    def get_nested_cli(self, path):
        return self.cli.get_list(os.path.join(path, "nested")) or ""

    def get_scripts_cli(self, path):
        return self.cli.get_list(os.path.join(path, "scripts")) or ""

    def get_all_cli(self, path):
        return self.cli.get_list(path) 


