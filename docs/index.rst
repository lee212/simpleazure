.. Simple Azure documentation master file, created by
   sphinx-quickstart on Tue Aug  6 22:36:05 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Simple Azure - Python library for Windows Azure
===============================================================================

Simple Azure enables template deployments of Microsoft Azure Services via the
new Azure Resource Manager and launching virtual machines via the classic
Service Management API. 407 community templates [1]_ from `Azure QuickStart
Templates <https://github.com/Azure/azure-quickstart-templates>`_ are included
to deploy software and infrasture with a few steps in Python and a classic
virtual machine service is supported with the azure-sdk-for-python legacy
package.  Simple Azure is currently in a development stage therefore new
features will be added from time to time and issues and bugs might be easily
found while you use Simple Azure. Check out the latest version from the `github
<https://github.com/lee212/simpleazure>`_ repository. Documentation is also
actively updated.

.. [1] as of 10/13/2016 from https://github.com/Azure/azure-quickstart-templates

Deploying a Template in Simple Azure ARM Mode
-------------------------------------------------------------------------------

From Azure QuickStart Template:

::

        >>> from simpleazure import SimpleAzure
        >>> saz = SimpleAzure()

        # aqst is for Azure QuickStart Templates
        >>> vm_sshkey_template = saz.aqst.get_template('101-vm-sshkey')

        # arm is for Azure Resource Manager
        >>> saz.arm.set_template(vm_sshkey_template)
        >>> saz.arm.set_parameter("sshKeyData", "ssh-rsa AAAB... hrlee@quickstart")
        >>> saz.arm.deploy()

From a custom template on github:

::

        >> url = "https://raw.githubusercontent.com/Azure-Samples/resource-manager-python-template-deployment/master/templates/template.json"
        >> saz.arm.deploy(template = url, param = { "sshKeyData": "ssh-rsa AAAB3Nza..." })

.. note:: For more about using ARM? check out :ref:`ref-arm`
.. note:: For more about deploying a custom Template? check out :ref:`ref-saz-template-deploy`
.. note:: For more about deploying Azure QuickStart Templates? check out :ref:`ref-aqst`

Caveats
-------------------------------------------------------------------------------

Simple Azure was started in 2013 but wasn't consistently updated which means
that some dated features may not work as expected. Relax, I am trying to get
Simple Azure back on track after these abandoned moments, so please report any
issues that you may encounter. I will try to fix or sort it out as quickly as
possible I can.

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

Docker Image 
-------------------------------------------------------------------------------

Simple Azure is available in Docker image to run.

- Simple Azure only:

.. code-block:: console

        docker pull lee212/simpleazure
        docker run -i -t lee212/simpleazure

- With IPython Notebook:

.. code-block:: console

        docker pull lee212/simpleazure_with_ipython
        docker run -i -t lee212/simpleazure_with_ipython


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


Contribution
-------------------------------------------------------------------------------

* Mailinglist (tbd)
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
