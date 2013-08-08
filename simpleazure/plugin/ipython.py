# -*- coding: utf-8 -*-

"""
plugin.ipython
~~~~~~~~~~~~~~~~~~~~~~~~

This module provides a Python library for Windows Azure Virtual Machines.

 :copyright: TBD
 :license: TBD

"""
import paramiko
import os

class IPython:

    def __init__(self):
        self.profile_name = "ssh"
        #self.init_ssh()

    def init_ssh(self):
        master = paramiko.SSHClient()
        master.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        master.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh",
                                                              "known_hosts")))
        self.ssh_master = master 

        ssh_engines = {}
        for engine in self.engines:
            ssh_engines[engine] = paramiko.SSHClient()
            ssh_engines[engine].set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_engines[engine].load_host_keys(os.path.expanduser(os.path.join("~",
                                                                               ".ssh",
                                                                               "known_hosts")))
        self.ssh_engines = ssh_engines

    def set_master(self, hostname):
        self.master = hostname

    def set_engines(self, hostnames):
        self.engines = hostnames

    def set_username(self, username):
        self.username = username

    def set_private_key(self, pkey_path):
        pkey = self._get_pkey(pkey_path)
        self.pkey = pkey

    def _get_pkey(self, path):
        """Return a new Paramiko key object based on the given private key

        :param path: the private key's path
        :type path: str
        :returns: a new key object

        """

        return paramiko.RSAKey.from_private_key_file(path)

    def connect_nodes(self):
        self.ssh_master.connect(self.master, username=self.username, pkey=self.pkey)

        for engine in self.engines:
            self.ssh_engines[engine].connect(engine, username=self.username,
                                             pkey=self.pkey)

    def create_profile(self):
        stdin, stdout, stderr = self.ssh_master.exec_command('ipython profile \
                                                             create \
                                                             --parallel \
                                                             --profile=%s' \
                                                             % self.profile_name)

    def run_ipcontroller(self):
        local_ip = "/sbin/ifconfig eth0 | grep \"inet addr\" | awk -F: '{print \
        $2}' | awk '{print $1}'"
        ssh_master_info = "%s@%s" % (self.username, self.master)
        profile = self.profile_name
        # With a paramiko channel (socket) function
        transport = self.ssh_master.get_transport()
        channel = transport.open_session()
        channel.exec_command('ipcontroller --ip=`%s` --profile=%s \
                             --enginessh=%s' % (local_ip, profile, ssh_master_info))

    def run_ipengine(self):
        for engine_name, ssh_engine in self.ssh_engines.iteritems():
            ssh_engine.exec_command('ipengine --file=%s' %
                                    self.get_targeted_json())

    def copy_json2engines(self):
        """Distribute the connection file (json) to each engine node so they can
        get access information to the master node.
        'scp' linux command used to copy"""

        ipengine_json_path = self.get_ipcontroller_engine_json()
        targeted_json_path = self.get_targeted_json()
        stdins, stdouts, stderrs = {}, {}, {}
        ssh_master_info = "%s@%s" % (self.username, self.master)
        for engine_name, ssh_engine in self.ssh_engines.iteritems():
            stdins[engine_name], stdouts[engine_name], stderrs[engine_name] = \
            ssh_engine.exec_command('scp %s:%s %s' % (ssh_master_info,
                                                      ipengine_json_path,
                                                      targeted_json_path))

    def get_ipcontroller_engine_json(self, profile=None):
        if not profile:
            profile = self.profile_name
        return "~/.config/ipython/profile_%s/security/ipcontroller-engine.json" % \
                profile


    def get_targeted_json(self, profile=None):
        if not profile:
            profile = self.profile_name
        return "~/.config/%s-ipcontroller-engine.json" % self.profile_name
