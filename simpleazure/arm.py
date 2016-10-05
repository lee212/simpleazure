# -*- coding: utf-8 -*-

"""
simpleazure.AzureResourceManagerTemplate

This module supports Azure Resource Manager with its Template in terms of deploying software stacks.

 :copyright:
 :license: 

"""

from urlparse import urlparse
import urllib, json
import os.path
from azure.common.credentials import ServicePrincipalCredentials as spc
from azure.mgmt.resource import ResourceManagementClient as rmc
from azure.mgmt.resource.resources.models import DeploymentMode as dm
from . import config
from . import utils


class Template(object):
    """Constructs a :class:`Template <Template>`.
    Returns :class:`Template <Template>` instance.

    Usage::

      >> from simpleazure.arm import Template as armt
      >> arm = armt()

    """

    location = config.DEFAULT_LOCATION
    resource_group = config.DEFAULT_RESOURCE_GROUP
    deployment = config.DEFAULT_DEPLOYMENT
    template = None
    parameters = None

    def __init__(self, subscription=None, client_id=None, secret=None, tenant=None):
        self.sshkey = SSHKey()
        self.get_credential(subscription, client_id, secret, tenant)

    def get_credential(self, subscription=None, client_id=None, secret=None, tenant=None):
        sid = os.getenv('AZURE_SUBSCRIPTION_ID', subscription)
        cid = os.getenv('AZURE_CLIENT_ID', client_id)
        tid = os.getenv('AZURE_TENANT_ID', tenant)
        sec = os.getenv('AZURE_CLIENT_SECRET', secret)
        self.cred = spc(client_id = cid, secret = sec, tenant = tid)
        self.client = rmc(self.cred, sid)

    def get_group_or_create(self):
        new_name = utils.get_rand_name()
        self.resource_group = new_name

    def deploy(self, template=None, param=None):
        self.set_sshkey()
        self.set_template(template)
        self.set_parameters(param)
        self.set_properties()
        self.update_rg()
        self.call_deploy()

    def terminate_deployment(self, resource_group=None, deployment=None):
        self.client.deployments.delete(resource_group or self.resource_group, deployment or self.deployment)

    def remove_rg(self, name):
        self.client.resource_groups.delete(name)

    def update_rg(self):
        res = self.client.resource_groups.create_or_update(
                self.resource_group,
                {
                    'location':self.get_location()
                    }
                )
        return res

    def call_deploy(self):
        res = self.client.deployments.create_or_update(
                self.resource_group,
                self.get_deployment_name(),
                self.deployment_properties )

        res.wait()
        return res

    def get_deployment_name(self):
        return self.deployment

    def get_location(self):
        """ Returns lower case without space """
        return self.location.lower().replace(" ", "")

    def set_properties(self):
        self.deployment_properties = {
                'mode': dm.incremental,
                'template': self.template,
                'parameters': self.parameters }

    def set_parameters(self, dictv):
        if self.parameters and dictv is None:
            return self.parameters

        self.parameters = self._get_parameters_with_value(dictv)

    def _get_parameters_with_value(self, dictv):
        parameters = {k: {'value': v} for k, v in dictv.items()}
        return parameters

    def set_sshkey(self, path=None):
        try:
            with open(os.path.expanduser(path or config.DEFAULT_SSH_KEY), "r") as f:
                self.sshkey.pubkey = f.read()
                return True
        except Exception as e:
            # debug / log 
            # print (e)
            return False

    def set_template(self, path_or_uri=None):
        if self.template and path_or_uri is None:
            return self.template

        if urlparse(path_or_uri).scheme is not "":
            template = json.loads(urllib.urlopen(path_or_uri).read())
        else:
            with open(path_or_uri, "r") as temp:
                template = temp.read()
        self.template = template

    def from_github(self, repo):
        # find repo
        # find json
        # get raw uri
        pass

    def default_param_from_github(self, repo):
        pass

    def update_param(self, data):
        pass

    def view_template(self):
        pass

    def view_info(self):
        pass
# Tips
#
# DeploymentMode: incremental | complete
# Deployments can be either Incremental or Complete. In Incremental mode,
# resources are deployed without deleting existing resources that are not
# included in the template. In complete mode resources are deployed and
# existing resources in the resource group not included in the template are
# deleted. The default mode is Incremental. 
# source: https://github.com/dx-ted-emea/Azure-Resource-Manager-Documentation/blob/master/ARM/Templates/Template_Deploy.md

class SSHKey(object):

    pvkey = None
    pubkey = None
    path = None
