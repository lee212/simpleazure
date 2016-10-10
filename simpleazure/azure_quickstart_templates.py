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
        return self.cli.get_list()

    def get_list_api(self):

        self.api.set_var("repo", self.git_repo)
        self.api.set_var("owner", self.git_owner)
        #res = [ item if item['type'] == "dir" for item in self.api.get_list() ]
        res = {}

        items = self.api.get_list()
        for item in items:
            if item['type'] != "dir":
                continue
            if item['name'] == ".github":
                continue
            try:
                # required files
                azuredeploy = self.get_azuredeploy(item['path'])
                parameters = self.get_parameters(item['path'])
                meta = self.get_metadata(item['path'])
            except:
                # If fails, skip to next
                continue
            etc = self.get_all(item['path'])
            nested = self.get_nested(item['path'])
            scripts = self.get_scripts(item['path'])
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

    def get_metadata(self, path):
        """Returns cotents of the metadata.json file from a path"""
        return self._get_json_contents(path + "/metadata.json")

    def get_azuredeploy(self, path):
        """Returns cotents of the azuredeploy.json file from a path"""
        return self._get_json_contents(path + "/azuredeploy.json")

    def get_parameters(self, path):
        """Returns cotents of the azuredeploy.parameters.json file from a path"""
        return self._get_json_contents(path + "/azuredeploy.parameters.json")

    def get_nested(self, path):
        """Returns nested templates from a path"""
        self.api.set_var("path", path + "/nested")
        return self.api.get_list() or ""

    def get_scripts(self, path):
        """Returns scripts from a path"""
        self.api.set_var("path", path + "/scripts")
        return self.api.get_list() or ""

    def get_all(self, path):
        """Returns all items from a path"""
        self.api.set_var("path", path)
        return self.api.get_list() 

    def _get_json_contents(self, path):
        self.api.set_var("path", path)
        data = json.loads(self.api.get_file())
        return data

