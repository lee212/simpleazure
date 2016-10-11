Deploying Azure Virtual Machine in Simple Azure ARM Mode
===============================================================================

Simpla Azure deploys a Ubuntu 16.04 VM using `the sample template <https://github.com/Azure-Samples/resource-manager-python-template-deployment/blob/master/templates/template.json>`_ from `Azure-Samples <https://github.com/Azure-Samples/resource-manager-python-template-deployment/>`_.

::

  >> import simpleazure as saz
  >> arm = saz.arm()
  >> url = "https://raw.githubusercontent.com/Azure-Samples/resource-manager-python-template-deployment/master/templates/template.json"
  >> arm.deploy(template = url, param = { "sshKeyData": "ssh-rsa AAAB3Nza..." })


A new deployment is completed on a resource group like::

.. image:: images/sampleazure.png


Deleting a deployment is::

  >> a.terminate_deployment()

Or removing a resource group is::

  >> a.remove_resource_group()

Overview
-------------------------------------------------------------------------------

Azure Virtual Machine is used to start via the servicemanagement API in Python
(which is now legacy or classic mode) with limited access to resources but new
Azure Resource Manager (ARM) supports launching a virtual machine with its
template for a service deployment. This page demonstrates how to start
a virtual machine in Simple Azure ARM mode with the template which contains
information of resoures to be deployed e.g.  Virtual Machine and Virtual
Network with Resource Groups. Simple Azure is able to load custom templates
from a file or a web and use the official community templates
`Azure-QuickStart-Templates
<https://github.com/Azure/azure-quickstart-templates/>_`.


.. note:: ARM does not support the classic version of virtual machines and
        cloud services which are only available via ServiceManagementAPI.
        VMs launched via ASM do not appear on ASM listing and vice versa.


ARM JSON Template
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

In addition, there are variables and outputs which are recommended to add
according to `the official templates
<https://github.com/Azure/azure-quickstart-templates>`_.

.. note:: For more information about templates including credential
        configuration, please see the Azure Resource Manager page here
        :ref:`ref-arm`

.. note:: official document of writing templates is here:
        https://azure.microsoft.com/en-us/documentation/articles/resource-group-authoring-templates/

Starting a VM with Simple Azure
-------------------------------------------------------------------------------

``arm`` sub package is added under ``simpleazure``. Try::

  >> import simpleazure
  >> arm = simpleazure.arm()

Credentials
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following Azure credentials are required to use ARM template on
SimpleAzure. Credentials for ASM (Azure Service Management API) are not valid
for ARM.

- subscription id       (equal to env name ``AZURE_SUBSCRIPTION_ID``)
- client id             (equal to env name ``AZURE_CLIENT_ID``)
- tenant id             (equal to env name ``AZURE_TENANT_ID``)
- client secret key     (equal to env name ``AZURE_CLIENT_SECRET``)

For more detail about credentials, see the ARM page here :ref:`ref-arm`

Deliver credential values as parameters like::

  >> sid = "5s3ag2s5-2aa1-4828-xxxx-9g8sw72w5w5g"
  >> cid = "5c5a3ea3-ap34-4pd0-xxxx-2p38ac00aap1"
  >> secret = "xxxxxxxxxxxxxxxxx"
  >> tid = "5e39a20e-c55a-53de-xxxx-2503a55et6ta"
  >> arm.set_credential(subscription = sid, client_id = cid, secret = secret, tenant = tid)

It is actually recommended to use environment variables like::

        $ cat <<EOF > ~/.saz/cred
        export AZURE_SUBSCRIPTION_ID=5s3ag2s5-2aa1-4828-xxxx-9g8sw72w5w5g
        export AZURE_CLIENT_ID=5c5a3ea3-ap34-4pd0-xxxx-2p38ac00aap1
        export AZURE_TENANT_ID=5e39a20e-c55a-53de-xxxx-2503a55et6ta
        export AZURE_CLIENT_SECRET=xxxx
        EOF

And then source it like:

::

        $ source ~/.saz/cred

With the environment variables, no parameters are necessary::

  >> arm.set_credential()

Load Template
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- URL
- FILE

Set Parameters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- SSH Pub Key
- TBD

Deployment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

  >> arm.deploy(url, parameters)

Termination
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Deleting a deployment is::

  >> arm.terminate_deployment()

Removing a resource group is ::

  >> arm.remove_resource_group()

Virtual Machine
-------------------------------------------------------------------------------

Starting a new virtual machine (*"Microsoft.Compute/virtualMachines"*)
requires Storage account and Network resources to store image file (.vhd) and
configure a network interface with a public ip address. (This is probably
different for Windows machines) Therefore, additional resources are expected in
the ``resources`` entity to complete vm deployment.

.. comment:: ``hardwareProfile``, ``storageProfile``, and ``networkProfile``.

It might be helpful to review virtual machine service from  one of the existing
templates. There is a template starting a VM with ssh public key:
`101-vm-ssh-key template
<https://github.com/Azure/azure-quickstart-templates/blob/master/101-vm-sshkey/azuredeploy.json>`_
, and the virtual machine service is defined like this in ``resources``::

        {
          "apiVersion": "2015-08-01",
          "type": "Microsoft.Compute/virtualMachines",
          "name": "simpleazure",
          "location": "centralus",
          "properties": {
            "hardwareProfile": {
            "vmSize": "Standard_DS2"
            },
            "osProfile": {
              "computerName": "simpleazure",
              "adminUsername": "ubuntu",
              "linuxConfiguration": {
                "disablePasswordAuthentication": "true",
                "ssh": {
                  "publicKeys": [
                    {
                      "keyData": "GEN-SSH-PUB-KEY"
                    }
                  ]
                }
              }
            },
            "storageProfile": {
              "imageReference": {
                "publisher": "Canonical",
                "offer": "UbuntuServer",
                "sku": "14.04-LTS",
                "version": "latest"
              },
              "osDisk": {
                "name": "osdisk",
                "vhd": {
                  "uri": "[variables('storage_uri')]"
                },
                "createOption": "FromImage"
              }
            },
            "networkProfile": {
              {
                "id": "[resourceId('Microsoft.Network/networkInterfaces', variables('nicName'))]"
              }
            }
          }
        }

There are other elements available but only required ones are demonstrated in
this example according to the `ARM schemas
<https://github.com/Azure/azure-resource-manager-schemas/blob/master/schemas/2015-08-01/Microsoft.Compute.json>`_


