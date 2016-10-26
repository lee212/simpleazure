# -*- coding: utf-8 -*-

"""
simpleazure.ansible_api

This module is from http://docs.ansible.com/ansible/developing_api.html
Slight changes are made to call ansible roles, plays after azure deployment

 :copyright:
 :license: 
          
"""
          
import json
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.playbook.play import Play
from ansible.playbook import Playbook
#from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.plugins.callback import CallbackBase

class ResultCallback(CallbackBase):
    """A sample callback plugin used for performing an action as results come in

    If you want to collect all results into a single object for processing at
    the end of the execution, look into utilizing the ``json`` callback plugin
    or writing your own custom callback plugin
    """
    def v2_runner_on_ok(self, result, **kwargs):
        """Print a json representation of the result

        This method could store the result in an instance attribute for retrieval later
        """
        host = result._host
        print json.dumps({host.name: result._result}, indent=4)

class AnsibleAPI(object):

    default_remote_user = "ubuntu"
    default_private_key_file = "~/.ssh/id_rsa"
    default_ssh_extra_args = '-o stricthostkeychecking=no'

    Options = namedtuple('Options', ['connection', 'module_path', 'forks',
        'become', 'become_method', 'become_user', 'check', 'remote_user',
        'private_key_file', 'ssh_extra_args', 'listhosts', 'listtasks',
        'listtags', 'syntax'])
    # initialize needed objects
    variable_manager = VariableManager()
    loader = DataLoader()
    options = Options(connection='ssh', module_path=None, forks=100,
            become=None, become_method=None, become_user=None, check=False,
            remote_user=default_remote_user,
            private_key_file=default_private_key_file,
            ssh_extra_args=default_ssh_extra_args, listhosts=None,
            listtasks=None, listtags=None, syntax=None) 
    passwords = dict(vault_pass='')

    # Instantiate our ResultCallback for handling results as they come in
    results_callback = ResultCallback()

    def __init__(self, hosts):
        # create inventory and pass to var manager
        self.inventory = Inventory(loader=self.loader,
                variable_manager=self.variable_manager, host_list=hosts)
        self.variable_manager.set_inventory(self.inventory)

    def playbook(self, pb):
        pbex = PlaybookExecutor(pb, inventory=self.inventory,
                variable_manager=self.variable_manager, loader=self.loader,
                options=self.options, passwords=self.passwords)
        self.pbex = pbex

    def run(self):

        try:
            results = self.pbex.run()
        except:
            pass

        return results
