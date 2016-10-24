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

# Test for getting ip address
from azure.mgmt.network import NetworkManagementClient as nmc

class AzureResourceManager(object):
    """Constructs a :class:`ARM <ARM>`.
    Returns :class:`ARM <ARM>` instance.

    Usage::

        >>> from simpleazure import SimpleAzure as saz
        >>> saz_client = saz()
        >>> saz_client.arm
        <simpleazure.azure_resource_manager.AzureResourceManager object at>

    """

    location = config.DEFAULT_LOCATION
    resource_group = config.DEFAULT_RESOURCE_GROUP
    deployment = config.DEFAULT_DEPLOYMENT
    template = None
    parameters = {}

    network = None

    def __init__(self, subscription=None, client_id=None, secret=None, tenant=None):
        self.get_credential(subscription, client_id, secret, tenant)
        self.template = Template()

    def get_credential(self, subscription=None, client_id=None, secret=None, tenant=None):
        sid = os.getenv('AZURE_SUBSCRIPTION_ID', subscription)
        cid = os.getenv('AZURE_CLIENT_ID', client_id)
        tid = os.getenv('AZURE_TENANT_ID', tenant)
        sec = os.getenv('AZURE_CLIENT_SECRET', secret)
        self.subscription_id = sid
        self.cred = spc(client_id = cid, secret = sec, tenant = tid)
        self.client = rmc(self.cred, sid)

    def get_group_or_create(self):
        new_name = utils.get_rand_name()
        self.resource_group = new_name

    def deploy(self, template=None, param=None):
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
        self._load_network_client()
        return self.network.get_access_info()

    def _load_network_client(self, refresh=False):
        if self.network:
            return self.network
        self.network = NMC(self.cred, self.subscription_id)
        self.network.set_resource_group(self.resource_group)
# Tips
#
# DeploymentMode: incremental | complete
# Deployments can be either Incremental or Complete. In Incremental mode,
# resources are deployed without deleting existing resources that are not
# included in the template. In complete mode resources are deployed and
# existing resources in the resource group not included in the template are
# deleted. The default mode is Incremental. 
# source: https://github.com/dx-ted-emea/Azure-Resource-Manager-Documentation/blob/master/ARM/Templates/Template_Deploy.md

class NMC(object):
    def __init__(self, credentials = None, subscription_id = None):
        if credentials and subscription_id:
            self.cred = credentials
            self.sid = subscription_id
        if self.cred and self.sid:
            self.client = nmc(self.cred, self.sid)

    def set_credentials(self, credentials, subscription_id):
        self.cred = credentials
        self.sid = subscription_id

    def set_resource_group(self, group_name):
        self.resource_group = group_name

    # public ip address in this example
    def get_access_info(self, resource_group=None):
        res = []
        try:
            ips = self.client.public_ip_addresses.list(resource_group or self.resource_group)
            # {'dns_settings': None, 'name': u'fp6mwq3k4ytsypublicip', 'tags': None, 'public_ip_address_version': u'IPv4', 'public_ip_allocation_method': u'Dynamic', 'resource_guid': u'24d9fc7a-8ff0-40da-9b88-e283e105c07c', 'provisioning_state': u'Succeeded', 'ip_address': u'40.83.13.177', 'etag': u'W/"1ea1dc32-6afc-4704-b927-d7f5db69d4da"', 'location': u'centralus', 'ip_configuration': <azure.mgmt.network.models.ip_configuration.IPConfiguration object at 0x7f56bd981890>, 'idle_timeout_in_minutes': 4, 'type': u'Microsoft.Network/publicIPAddresses', 'id': u'/subscriptions/6b3cf2b5-2cc1-4828-b5e0-9f8be72e6e6f/resourceGroups/saz-rg/providers/Microsoft.Network/publicIPAddresses/fp6mwq3k4ytsypublicip'}
            for ip in ips:
                res.append(ip.ip_address)
            return res
        except:
            return res

