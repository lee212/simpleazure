# -*- coding: utf-8 -*-

"""
simpleazure.simpleazure.SimpleAzure
~~~~~~~~~~~~~~~~~~~~~~~~

This module provides a classic Python library for Windows Azure Virtual
Machines.

 :copyright: 2016, Hyungro Lee (hroe.lee@gmail.com)
 :license: GPLv3

"""

from .azure_service_management import AzureServiceManagement
from .azure_resource_manager import AzureResourceManager
from .azure_quickstart_templates import AzureQuickStartTemplates

class SimpleAzure(object):
    arm = AzureResourceManager()
    asm = AzureServiceManagement()
    aqst = AzureQuickStartTemplates()
