# -*- coding: utf-8 -*-

"""
simpleazure.arm

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
from template.template import Template

class ARM(object):
    """Constructs a :class:`ARM <ARM>`.
    Returns :class:`ARM <ARM>` instance.

    Usage::

      >> from simpleazure.arm import ARM as armt
      >> arm = armt()

    """

    location = config.DEFAULT_LOCATION
    resource_group = config.DEFAULT_RESOURCE_GROUP
    deployment = config.DEFAULT_DEPLOYMENT
    template = None
    parameters = {}

    def __init__(self, subscription=None, client_id=None, secret=None, tenant=None):
        self.sshkey = SSHKey()
        self.get_credential(subscription, client_id, secret, tenant)
        self.template = Template()

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
        self.sshkey.set_pubkey()
        self.set_template(template)
        self.set_parameters(param)
        self.set_deployment_properties()
        self.update_rg()
        return self.call_deploy()

    def terminate_deployment(self, resource_group=None, deployment=None):
        self.client.deployments.delete(resource_group or self.resource_group, deployment or self.deployment)

    def remove_rg(self, name=None):
        return self.remove_resource_group(name)

    def remove_resource_group(self, name=None):
        return self.client.resource_groups.delete(name or self.resource_group)

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

    def set_deployment_properties(self):
        self.deployment_properties = {
                'mode': dm.incremental,
                'template': self.template['azuredeploy'],
                'parameters': self.parameters }

    def add_parameter(self, param):
        """Set a single parameter"""
        param_with_value = self._get_parameters_with_value(param)
        self.parameters.update(param_with_value)
        return self.parameters

    def set_parameters(self, params):
        if self.parameters and params is None:
            return self.parameters

        self.parameters = self._get_parameters_with_value(params)
        return self.parameters

    def _get_parameters_with_value(self, params):
        parameters = {k: {'value': v} for k, v in params.items()}
        return parameters
 
    def set_template(self, path_or_uri=None):
        if self.template and path_or_uri is None:
            return self.template

        if urlparse(path_or_uri).scheme is not "":
            template = json.loads(urllib.urlopen(path_or_uri).read())
        else:
            with open(path_or_uri, "r") as temp:
                template = temp.read()
        self.template['azuredeploy'] = template

    def load_template(self, template):
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

#extra
class SSHKey(object):

    pvkey = None
    pubkey = None
    pubkey_path = None
    pvkey_path = None

    default_path = { 
            'pvkey': "~/.ssh/id_rsa",
            'pubkey': "~/.ssh/id_rsa.pub" 
            }

    def __init__(self, path=None):
        self.set_pubkey(path)

    def set_pubkey(self, path=None):
        try:
            path = os.path.expanduser(path or self.default_path['pubkey'])
            with open(path, "r") as f:
                self.pubkey = f.read()
                f.close()
                self.pubkey_path = path
                return True
        except Exception as e:
            # debug / log 
            # print (e)
            return False



