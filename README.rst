Simple Azure
===============================================================================

Simple Azure deploys Azure Templates and launches Virtual Machine with Service
Management API with a few steps like other cloud providers e.g. AWS.
[Documentation](https://simple-azure.readthedocs.org/)

Docker Image 
-------------------------------------------------------------------------------

Simple Azure is available in Docker image to run.

- Simple Azure only:

.. code-block:: console

        docker run -i -t lee212/simpleazure

- With IPython Notebook:

.. code-block:: console

        docker run -d -p 8888:8888 lee212/simpleazure_with_ipython

Open a browser with the port number **8888**.

Installation
-------------------------------------------------------------------------------

From github.com:

.. code-block:: console

   git clone https://github.com/lee212/simpleazure.git
   cd simpleazure
   pip install -r requirements.txt
   python setup.py install

from Pypi:

.. code-block:: console

   pip install simpleazure

QuickStart
-------------------------------------------------------------------------------

Starting `101-vm-sshkey
<https://github.com/Azure/azure-quickstart-templates/tree/master/101-vm-sshkey>`_
template:

.. code-block:: pycon

        >>> from simpleazure import SimpleAzure
        >>> saz = SimpleAzure()

        # aqst is for Azure QuickStart Templates
        >>> vm_sshkey_template = saz.aqst.get_template('101-vm-sshkey')

        # arm is for Azure Resource Manager
        >>> saz.arm.set_template(vm_sshkey_template)
        >>> saz.arm.set_parameter("sshKeyData", "ssh-rsa AAAB... hrlee@quickstart")
        >>> saz.arm.deploy()



Caveats
-------------------------------------------------------------------------------

- Classic (legacy) Python SDK is based on
  https://github.com/Azure/azure-sdk-for-python/blob/master/azure-servicemanagement-legacy
- Virtual Machines, Cloud Services and Storage are only used in the classic mode to deploy virtrual machines.

Prerequisite
-------------------------------------------------------------------------------

- Azure Cli installation

.. code-block:: console

    sudo apt-get install nodejs-legacy
    sudo apt-get install npm
    sudo npm install -g azure-cli

Account Setup for ASM
-------------------------------------------------------------------------------

- Open a browser to http://go.microsoft.com/fwlink/?LinkId=254432
- ``*-DD-MM-YYYY-credentials.publishsettings`` is downloaded on a local
  directory
- Run ``azure config mode as`` # To run azure cli tool via the classic service
  management certificate.
- Run ``azure account import <publishsettings file>``
- Run ``azure account cert export ~/.azure/managementCertificate.pem``

Example (classic mode for launching VMs)
-------------------------------------------------------------------------------

Create a VM on Windows Azure
(ubuntu 14.04 is a default image)

.. code-block:: python

        from simpleazure import SimpleAzure as saz

        azure = saz()
        azure.asm.create_vm()

Status can be seen here.

.. code-block:: pycon

        print vars(azure.get_status())
        {'error': None, 'http_status_code': u'200', 'id': u'', 'status': u'Succeeded'}
or

.. code-block:: pycon

        print vars(azure.get_deployment())
        {'configuration': u'<ServiceConfiguration xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://schemas.microsoft.com/ServiceHosting/2008/10/ServiceConfiguration">\r\n  <Role name="myvm-20735">\r\n    <Instances count="1" />\r\n  </Role>\r\n</ServiceConfiguration>',
         'created_time': u'2013-07-22T16:10:18Z',
         'deployment_slot': u'Production',
         'extended_properties': {},
         'input_endpoint_list': None,
         'label': u'bXl2bS0yMDczNQ==',
         'last_modified_time': u'',
         'locked': False,
         'name': u'myvm-20735',
         'persistent_vm_downtime_info': None,
         'private_id': u'17071ce8bea345cf1575341c8510c84a',
         'role_instance_list': <azure.servicemanagement.RoleInstanceList at 0x333b5d0>,
         'role_list': <azure.servicemanagement.RoleList at 0x333b610>,
         'rollback_allowed': False,
         'sdk_version': u'',
         'status': u'Running',
         'upgrade_domain_count': u'1',
         'upgrade_status': None,
         'url': u'http://myvm-20735.cloudapp.net/'}

Example for multiple deployment (classic)
-------------------------------------------------------------------------------

cluster() function helps to deploy several VMs at once.


.. code-block:: python

        azure = saz()
        azure.asm.create_cluster()

        my-cluster-vm-0-87412
        {'request_id': '88c94c00288d42acaf877783f09c4558'}
        my-cluster-vm-1-61293
        {'request_id': 'abfd563c2c4f4926872b6b1dba27a93b'}
        my-cluster-vm-2-96085
        {'request_id': '29b55f6cb5e94cfdbf244a7c848c854d'}
        my-cluster-vm-3-46927
        {'request_id': 'b1a3446ebafe47a295df4c9d1b7d743c'}

Example for multiple deployment with Azure Data Science Core
-------------------------------------------------------------------------------

Deploy 5 VMs with Azure Data Science Core at West Europe 


.. code-block:: python

        azure = saz()
        q = azure.asm.get_registered_image(name="Azure-Data-Science-Core")
        azure.asm.set_image(image=q,refresh=True)
        azure.asm.set_location("West Europe")
        azure.asm.create_cluster(num=5)

List of VMs
-------------------------------------------------------------------------------

.. code-block:: python

        vars(azure.asm.list_deployments().hosted_services)

Terminating VM
-------------------------------------------------------------------------------

.. code-block:: python

        azure.asm.delete_vm()

or

.. code-block:: python

        azure.asm.delete_vm('vm-name')

Clustering
-------------------------------------------------------------------------------

TBD


Contact
-------------------------------------------------------------------------------

hroe.lee at gmail.com
