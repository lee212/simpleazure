# -*- coding: utf-8 -*-

"""
simpleazure.arm

This module supports Azure Resource Manager with its Template in terms of
deploying software stacks.

Caveats: Not all Azure services are supported. Currently supported resources
    from azure.mgmt are:
    - ResourceManagementClient
    - SubscriptionClient
    Any resources related to start a virtual machine will be added

 :copyright:
 :license: 

"""

from urlparse import urlparse
import urllib, json
import os.path
import azure
from azure.common.credentials import ServicePrincipalCredentials as spc
from azure.mgmt.resource import ResourceManagementClient as rmc
from azure.mgmt.resource.resources.models import DeploymentMode as dm
from azure.mgmt.resource import SubscriptionClient as sc
from . import config
from . import utils
from template.template import Template
from .azure_network_management import AzureNetworkManagement as nmc
import pandas as pd
import time

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
    default_tag = { 'SimpleAzure': 'default' }
    selected_service = "resource_groups"

    def __init__(self, subscription=None, client_id=None, secret=None, tenant=None):
        self.get_credential(subscription, client_id, secret, tenant)
        # resource management client as rmc
        self.client = rmc(self.cred, self.subscription_id)
        # subscription client as sc
        self.s_client = sc(self.cred)
        self.template = Template()

    def get_credential(self, subscription=None, client_id=None, secret=None, tenant=None):
        sid = os.getenv('AZURE_SUBSCRIPTION_ID', subscription)
        cid = os.getenv('AZURE_CLIENT_ID', client_id)
        tid = os.getenv('AZURE_TENANT_ID', tenant)
        sec = os.getenv('AZURE_CLIENT_SECRET', secret)
        self.subscription_id = sid
        self.cred = spc(client_id = cid, secret = sec, tenant = tid)

    # Test code
    def create(self, service_name=None, **kwargs):
        if service_name is None:
            service_name = self.selected_service

    # Test code
    def delete(self, service_name=None, **kwargs):
        if service_name is None:
            service_name = self.selected_service

    # Test code
    def list(self, service_name=None):
        if service_name is None:
            service_name = self.selected_service
        func = getattr(self.client, service_name)
        func = getattr(func, "list")
        res = func()
        new = []
        for i in res:
            new.append(pd.Series(i.__dict__))

        return new

    # Test code
    def get(self, service_name=None, **kwargs):
        if service_name is None:
            servie_name = self.selected_service
        func = getattr(self.client, service_name)
        func = getattr(func, "get")
        res = func(**kwargs)
        new = []
        for i in res:
            new.append(pd.Series(i.__dict__))

        return new

    def get_resource_group_name(self):
        return self.resource_group

    def set_resource_group_name(self, name):
        result_check = self.client.resource_groups.check_existence(name)
        if not result_check:
            return result_check
        self.resource_group = name
        return result_check

    def list_available_locations(self):
        locations = self.s_client.subscriptions.list_locations(self.subscription_id)
        return pd.Series(list(locations))


    def get_group_or_create(self):
        new_name = utils.get_rand_name()
        self.resource_group = new_name

    def deploy(self, template=None, param=None):
        self.set_template(template)
        self.set_parameters(param)
        self.set_deployment_properties()
        start = time.time()
        self.update_resource_group()
        result = self.call_deploy()
        end = time.time()
        print ("{0:.2f} elapsed time for the deployment".format (end - start))
        return result

    def terminate_deployment(self, resource_group=None, deployment=None):
        self.client.deployments.delete(resource_group or self.resource_group, deployment or self.deployment)

    def remove_rg(self, name=None):
        return self.remove_resource_group(name)

    def remove_resource_group(self, name=None):
        return self.client.resource_groups.delete(name or self.resource_group)

    def update_resource_group(self):
        res = self.client.resource_groups.create_or_update(
                self.resource_group,
                {
                    'location':self.get_location(),
                    'tags': self.default_tag
                },
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

    def set_location(self, location):
        """ Set location with a input location 

            location: string
            location: azure.mgmt.resource.subscriptions.models.location.Location
        
        """
        if isinstance(location, str):
            self.location = location.lower().replace(" ", "")
        elif isinstance(location, azure.mgmt.resource.subscriptions.models.location.Location):
            self.location = location.name

    def get_location(self, name=None):
        """ Returns lower case without space """
        if name:
            return pd.Series(vars(name))
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
        parameters = {k: {u'value': v} for k, v in params.items()}
        return parameters
 
    def set_template(self, path_or_uri=None):
        if self.template and path_or_uri is None:
            return self.template

        if urlparse(path_or_uri).scheme is not "":
            template = json.loads(urllib.urlopen(path_or_uri).read())
        else:
            with open(os.path.expanduser(path_or_uri), "r") as temp:
                template = json.loads(temp.read())
        self.template['azuredeploy'] = template
        #self.set_parameters(template['parameters'])

    def load_template(self, template):
        self.template = template
        self.parameters = template['parameters']['parameters']

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
        self.network = nmc(self.cred, self.subscription_id)
        self.network.set_resource_group(self.resource_group)

    def export_template(self, group_name=None, deployment_name=None):
        return self._export_template()

    def _export_template(self):
        return self.template

    def _export_template_api(self, group_name=None, deployment_name=None):
        return self.client.deployments.export_template(group_name or
                self.resource_group, deployment_name or
                self.get_deployment_name())

# Tips
#
# DeploymentMode: incremental | complete
# Deployments can be either Incremental or Complete. In Incremental mode,
# resources are deployed without deleting existing resources that are not
# included in the template. In complete mode resources are deployed and
# existing resources in the resource group not included in the template are
# deleted. The default mode is Incremental. 
# source: https://github.com/dx-ted-emea/Azure-Resource-Manager-Documentation/blob/master/ARM/Templates/Template_Deploy.md


