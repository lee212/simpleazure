Start Azure Virtual Machine in SimpleAzure ARM Mode
===============================================================================

This page demonstrates how to start a virtual machine using Azure Resource
Manager Templates which contains information of resoures to be deployed e.g.
Virtual Machine and Virtual Network with Resource Groups. Simple Azure is
recently updated to support ARM mode to deploy infrastructure with custom and
official templates.


.. note:: ARM does not support the classic version of virtual machines and
        cloud services which are only available via Azure classic portal.
        Classic version runs with Azure Service Management (ASM) which is
        exclusive to ARM according to Azure CLI.

Overview of ARM Template
-------------------------------------------------------------------------------

Azure Resource Template uses JSON format to describe its parameters, variables,
resources and outputs. For example, the blank template looks like::

  {
     "$schema": "http://schema.management.azure.com/schemas/2015-01-01/deploymentTemplate.json#",
     "contentVersion": "1.0.0.0",
     "parameters": {  },
     "resources": [  ]
  }

* This basic template is obtained from the azure portal:
  https://portal.azure.com/#create/Microsoft.MyGallery

- ``resources`` contains definition of azure services to be deployed e.g.
  Virtual Machine. Also, this ``resources`` entity is mandatory.
- ``parameters`` contains input values which allow you to provide when template
  is deployed.

In addition, there are variables and outputs which are recommended like `the
official templates
<https://github.com/Azure/azure-quickstart-templates>`_.

.. note:: For more information about template including credential
        configuration, please see the Azure Resource Manager page here :ref:`ref-arm`

.. note:: official document is here:
        https://azure.microsoft.com/en-us/documentation/articles/resource-group-authoring-templates/

Virtual Machine
-------------------------------------------------------------------------------

Starting a VM with SimpleAzure
-------------------------------------------------------------------------------

Credentials
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following Azure credentials are required to use ARM template on SimpleAzure.

- subscription id       (equal to env name ``AZURE_SUBSCRIPTION_ID``)
- client id             (equal to env name ``AZURE_CLIENT_ID``)
- tenant id             (equal to env name ``AZURE_TENANT_ID``)
- client secret key     (equal to env name ``AZURE_CLIENT_SECRET``)

For more detail about credentials, see the ARM page here :ref:`ref-arm`

via Azure CLI
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
