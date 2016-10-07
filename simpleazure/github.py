# -*- coding: utf-8 -*-

"""
simpleazure.git

This module supports github API

 :copyright:
 :license: 

"""

import re
import json
import requests
import inspect

class Github(object):
    """Constructs a :class:`Github <Github>`.
    Returns :class:`Github <Github>` instance.

    Disclaimer: This class does not cover every API calls from github.
    'Repositories' and 'Search' are mainly used to support listing and
    searching contents related to Azure Resource Manager Templates.

    Usage::

    """

    base_url = "https://api.github.com"
    request_url = ""


    # Define api_path and exec_str when you add a new api call
    api_path = {
            "get_file": "/repos/:owner/:repo/contents/:path",
            "get_list": "/repos/:owner/:repo/contents/"
            }

    exec_results = {
            "get_file": "self.results['content'].decode('base64')",
            "get_list": "self.results",
            "search_code": "self.results",
            }

    def __init__(self):
        pass

    def set_repo(self, repo):
        self.repo = repo

    def search_code(self, word):
        """https://developer.github.com/v3/search/#search-code
       
        GET /search/code

        in Qualifies which fields are searched. With this qualifier you can restrict the search to the file contents (file), the file path (path), or both.
        language Searches code based on the language it's written in.
        fork Specifies that code from forked repositories should be searched (true). Repository forks will not be searchable unless the fork has more stars than the parent repository.
        size Finds files that match a certain size (in bytes).
        path Specifies the path prefix that the resulting file must be under.
        filename Matches files by a substring of the filename.
        extension Matches files with a certain extension after a dot.
        user or repo Limits searches to a specific user or repository.
        """
        self.action = inspect.stack()[0][3]
        # TODO
        # Create a function to manage parameters in a generic way
        request_url = self.base_url + "/search/code?q="+word
        if self.repo:
            request_url += "+repo:" + self.repo
        self.request_url = request_url
        if self.run_api():
            return self.get_results()

    def set_var(self, key, value):
        exec("self." + key + "='" + value + "'")

    def unset_var(self, key):
        exec("self." + key + "=''")

    def get_file(self):
        """https://developer.github.com/v3/repos/contents/#get-contents

        GET /repos/:owner/:repo/contents/:path

        This is for a file

        """
        self.action = inspect.stack()[0][3]
        api_path = self._get_api_path(self.action)
        request_url = self._fill_in_path(api_path)
        self.request_url = request_url
        if self.run_api():
            return self.get_results()

    def get_list(self):
        """https://developer.github.com/v3/repos/contents/#get-contents

        GET /repos/:owner/:repo/contents/:path

        This is for a directory

        """
        return self._exec()

    def _exec(self):
        self.action = inspect.stack()[1][3]
        api_path = self._get_api_path(self.action)
        request_url = self._fill_in_path(api_path)
        self.request_url = request_url
        if self.run_api():
            return self.get_results()

    def get_results(self):
        ret = None
        exec_str = self.exec_results[self.action]
        try:
            exec("ret = " + exec_str)
        except:
            ret = self.results
        return ret

    def _get_api_path(self, action_name):
        try:
            return self.api_path[action_name]
        except KeyError as e:
            print ("{0} is not defined, is it valid API call according to" + \
                    "'https://developer.github.com/v3/'?".format(action_name))

    def _fill_in_path(self, api_path):
        new = api_path 
        try:
            for m in re.finditer(r":\w+", api_path):
                new = re.sub(m.group(0), eval("self." + m.group(0)[1:]), new)
            return self.base_url + new
        except NameError as e:
            print ("{0} is not defined".format(m.group(0)))

    def run_api(self):
        if not self.request_url:
            raise "api path is not defined"

        res = requests.get(self.request_url)
        if res.ok:
            self.results = json.loads(res.text)
            return True
        return False

    def run_direct(self, url):
        self.request_url = url
        if self.run_api():
            return self.get_results()
        
    def reset(self):
        self.request_url = ""
        self.repo = ""
        self.action = ""

    def clear(self):
        self.reset()
