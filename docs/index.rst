.. Simple Azure documentation master file, created by
   sphinx-quickstart on Tue Aug  6 22:36:05 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Simple Azure - Python Library for Windows Azure
===============================================================================

Simple Azure is a Python library for Microsoft Azure Services including Virtual
Machine (VM) to provision resources in a simple way. Infrastructure
provisioning is supported now with the new Azure Resource Manager (ARM)
Templates, therefore you can describe and share your application with
infrastructure in a JSON format template to reproduce same infrastructure
constantly. Launching classic virtual machines is supported using the Azure
Service Management (ASM) API which is now called classic or legacy mode.  

Simple Azure includes 407 community templates [1]_ from `Azure QuickStart
Templates <https://github.com/Azure/azure-quickstart-templates>`_ 
to deploy software and infrastructure ranging from a simple linux VM deployment
(i.e. `101-vm-simple-linux
<https://github.com/Azure/azure-quickstart-templates/tree/master/101-vm-simple-linux>`_)
to Azure Container Service cluster with a DC/OS orchestrator (i.e.
`101-acs-dcos
<https://github.com/Azure/azure-quickstart-templates/tree/master/101-acs-dcos>`_).
You can import, export, search, modify, review and deploy these templates using
Simple Azure and get information about deployed services in resource groups.
Initial scripts or automation tools can be triggered after a completion of
deployements therefore your software stacks and applications are installed and
configured to run your jobs or launch your services.

A classic virtual machine service is supported with the azure-sdk-for-python
legacy package to create a single virtual machine (VM) and multiple VMs.

Simple Azure is currently in a development stage therefore new features will be
added from time to time and issues and bugs might be easily found while you use
Simple Azure. Check out the latest version from the `github
<https://github.com/lee212/simpleazure>`_ repository. Documentation is also
actively updated.

.. [1] as of 10/13/2016 from https://github.com/Azure/azure-quickstart-templates

Deploying a Template in Simple Azure ARM Mode
-------------------------------------------------------------------------------

Starting a single Linux VM with SSH key from Azure QuickStart Template is:

::

        >>> from simpleazure import SimpleAzure
        >>> saz = SimpleAzure()

        # aqst is for Azure QuickStart Templates
        >>> vm_sshkey_template = saz.aqst.get_template('101-vm-sshkey')

        # arm is for Azure Resource Manager
        >>> saz.arm.set_template(vm_sshkey_template)
        >>> saz.arm.set_parameter("sshKeyData", "ssh-rsa AAAB... hrlee@quickstart")
        >>> saz.arm.deploy()

Starting a sample VM from a custom template URL is:

::

        >> url = "https://raw.githubusercontent.com/Azure-Samples/resource-manager-python-template-deployment/master/templates/template.json"
        >> saz.arm.deploy(template = url, param = { "sshKeyData": "ssh-rsa AAAB3Nza...", 'dnsLabelPrefix':"simpleazure", 'vmName':'simpleazure-first-vm'}) })

.. note:: For more about using ARM? check out :ref:`ref-arm`
.. note:: For more about deploying a custom Template? check out :ref:`ref-saz-template-deploy`
.. note:: For more about deploying Azure QuickStart Templates? check out :ref:`ref-aqst`

Docker Image 
-------------------------------------------------------------------------------

Simple Azure is available in a Docker image to run.

- With IPython Notebook:

.. code-block:: console

        docker run -d -p 8888:8888 lee212/simpleazure_with_ipython

Open a browser with the port number **8888**.

- Simple Azure only:

.. code-block:: console

        docker run -i -t lee212/simpleazure


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

Deploying Azure Virtual Machines (classic mode)
-------------------------------------------------------------------------------

Three lines are required to deploy Window Azure Virtual Machine in Simple
Azure.

.. code-block:: python

   from simpleazure.simpleazure import SimpleAzure as saz

   azure = saz()
   azure.create_vm()
   
.. raw:: html

   <iframe width="560" height="315" src="//www.youtube.com/embed/pHG_gmnc6qI" frameborder="0" allowfullscreen></iframe>

Caveats
-------------------------------------------------------------------------------

Simple Azure was started in 2013 but wasn't consistently updated which means
that some dated features may not work as expected. Relax, I am trying to get
Simple Azure back on track after these abandoned moments, so please report any
issues that you may encounter. I will try to fix or sort it out as quickly as
possible I can.

Not supported features:

- Python 3 is NOT supported

Obsolete features (might be revived later):

- virtual cluster
- IPython cluster with the plugin
- Access to the open VM image repository (VM Depot)

If you are looking for a classic mode launching a virtual machine, you can get
started with :doc:`Quickstart </quickstart>` and then learn more through
:doc:`Tutorial </tutorial>` that shows how to deploy and utilize
Azure Virtual Machines with Simple Azure.  :doc:`Installation </installation>`
and :doc:`Configuration </configuration>` helps you get Simple Azure installed
on your machine and :doc:`Command </command>` describes how to use Simple Azure
on the python shell. You can find resources :doc:`here </deliverables>`.



Contribution
-------------------------------------------------------------------------------

* `issues <https://github.com/lee212/simpleazure/issues>`_


Contents
-------------------------------------------------------------------------------

.. toctree::
   :maxdepth: 1

   arm
   templates
   azure_quickstart_templates
   quickstart
   tutorial
   installation
   command
   configuration
   deliverables

.. comments::

        Indices and tables
        -------------------------------------------------------------------------------

        * :ref:`genindex`
        * :ref:`modindex`
        * :ref:`search`
