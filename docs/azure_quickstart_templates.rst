.. _ref-aqst:

Deploying Azure QuickStart Templates
===============================================================================
:

.. code-block:: pycon

        >>> from simpleazure.azure_quickstart_templates import AzureQuickStartTemplates as aqst
        >>> aqst = aqst.AzureQuickStartTemplate()
        >>> vm_sshkey_template = aqst.get_template('101-vm-sshkey')

        >>> from simpleazure import arm
        >>> arm = arm.ARM()
        >>> arm.set_parameter("sshKeyData", "ssh-rsa AAAB... hrlee@quickstart")
        >>> arm.set_template(vm_sshkey_template)
        >>> arm.deploy()

Azure provides 407 community templates [1]_ from starting a single virtual
machine (e.g. 101-vm-sshkey) to hadoop clusters with Apache Spark (e.g.
hdinsight-apache-spark) and Simple Azure supports deploying these templates in
Python with additional options like a template search.

The example above shows that Simple Azure loads ``101-vm-sshkey`` template from
the *azure-quickstart-templates* github repository and deploys it with a
required parameter, ssh public key string (*sshKeyData*).

.. [1] as of 10/13/2016 from https://github.com/Azure/azure-quickstart-templates

Overview
-------------------------------------------------------------------------------

This page describes use of `Azure QuickStart Templates
<https://github.com/Azure/azure-quickstart-templates>`_ in Python with Simple
Azure which supports - template search, list, load, view and deployment on
Microsoft Azure. 

A template in the azure quickstart is served in a single directory with
required json files to describe resource deployments. Simple Azure provides
template information in Python based on the directory name and the files in the
directory. Metadata, for example, is supplied by:

:

.. code-block:: pycon

        >>> vm_sshkey_template.metadata()
        dateUpdated                                               2015-06-05
        description        This template allows you to create a Virtual M...
        githubUsername                                             squillace
        itemDisplayName     Deploy a Virtual Machine with SSH rsa public key
        summary             Deploy a Virtual Machine with SSH rsa public key

This output is from ``101-vm-sshkey`` template and ``metadata()`` returns
its description such as date, description, and github username of the template.

``get_templates()`` provides listing all templates which is also based on the
diretory name and the metadata like:

:

.. code-block:: pycon

        >>> templates = aqst.get_templates()
        >>> templates.ten()
        100-blank-template                                                                  Blank Template
        101-acs-dcos                                                       Azure Container Service - DC/OS
        101-acs-mesos                                                      Azure Container Service - DC/OS
        101-acs-swarm                                                      Azure Container Service - Swarm
        101-app-service-certificate-standard             Create and assign a standard App Service Certi...
        101-app-service-certificate-wildcard             Create and assign a wildcard App Service Certi...
        101-application-gateway-create                                       Create an Application Gateway
        101-application-gateway-public-ip                     Create an Application Gateway with Public IP
        101-application-gateway-public-ip-ssl-offload         Create an Application Gateway with Public IP
        101-automation-runbook-getvms                    Create Azure Automation Runbook to retrieve Az...

Choose one of the templates using Python dict data format, for example,
``101-acs-dcos`` template (2nd template in the listing) is displayed by:

:

.. code-block:: pycon
        >>> templates['101-acs-dcos'].metadata()
        dateUpdated                                               2016-02-18
        description        Deploy an Azure Container Service instance for...
        githubUsername                                              rgardler
        itemDisplayName                      Azure Container Service - DC/OS
        summary            Azure Container Service optimizes the configur...

More options are available to search, load and deploy templates via Simple Azure
and the following sections demonstrate these options with examples.

.. comment::

        - statistics for deploying time, number of resources, price tags, options, limitations (versions, os distribution)
          - possible more information of sizes, image,
        - statistics for technologies
        - sub templates (probably supported?) 

Searching Template
-------------------------------------------------------------------------------

Simple Azure supports a template search from the Azure QuickStart Templates
with a keyword. Let's find templates that use 'rhel' (Red Hat Enterprise Linux)
in a description. 

:

.. code-block:: pycon

        >>> rhel_templates = aqst.search("rhel")

It found 13 templates and the first ten items are: 

:

.. code-block:: pycon

        >>> len(rhel_templates)
        13

        >>> rhel_templates.ten()
        101-vm-full-disk-encrypted-rhel       Red Hat Enterprise Linux 7.2 VM (Fully Encrypted)
        101-vm-simple-rhel                    Red Hat Enterprise Linux VM (RHEL 7.2 or RHEL ...
        201-encrypt-running-linux-vm                   Enable encryption on a running Linux VM.
        create-hpc-cluster-linux-cn              Create an HPC cluster with Linux compute nodes
        intel-lustre-client-server/scripts
        intel-lustre-clients-on-centos          Intel Lustre clients using CentOS gallery image
        openshift-origin-rhel                 OpenShift Origin on RHEL (On Demand image) or ...
        openshift-origin-rhel/nested
        sap-2-tier-marketplace-image            2-tier configuration for use with SAP NetWeaver
        vsts-tomcat-redhat-vm                 Red Hat Tomcat server for use with Team Servic...

Next items are displayed by calling ``ten()`` again:

:

.. code-block:: pycon

        >>> rhel_templates.ten()
        intel-lustre-clients-vmss-centos       Azure VM Scale Set as clients of Intel Lustre
        sap-3-tier-marketplace-image         3-tier configuration for use with SAP NetWeaver
        zabbix-monitoring-cluster/scripts

Template Details
-------------------------------------------------------------------------------

Simple Azure provides Template() object functions to quickly review template
details such as required parameters, template descriptions and resource
information. The available functions are:

- [template object].metadata()
- [template object].parameters()
- [template object].resources()
- [template object].dependson()
- [template object].dependson_print()

.. note:: each template is served with at least three files i.e. 

- azuredeploy.json (service deployment)
- azuredeploy.parameters.json (parameter information)
- metadata.json (description of template)

Simple Azure runs by loading these files when it's imported in python.

Metadata
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

See metadata of the template ``101-vm-simple-rhel`` from the search results
above:

:

.. code-block:: pycon

        >>> rhel_templates['101-vm-simple-rhel'].metadata()
        dateUpdated                                               2016-02-23
        description        This template will deploy a Red Hat Enterprise...
        githubUsername                                            BorisB2015
        itemDisplayName    Red Hat Enterprise Linux VM (RHEL 7.2 or RHEL ...
        summary            This template will deploy RedHat (RHEL) VM, us...

        >>> rhel_templates['101-vm-simple-rhel'].metadata().description
        u'This template will deploy a Red Hat Enterprise Linux VM (RHEL 7.2 or
        RHEL 6.7), using the Pay-As-You-Go RHEL VM image for the selected
        version on Standard D1 VM in the location of your chosen resource group
        with an additional 100 GiB data disk attached to the VM. Additional
        charges apply to this image - consult Azure VM Pricing page for
        details.'

Here, ``metadata()`` returns ``101-vm-simple-rhel`` template description in
Pandas Series format and full description text is visible like python class
variable (metadata().description).


This information is from ``matadata.json`` and returned by Pandas Series

:

::

        [template object].metadata()            # pandas Series


Parameters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We may want to know what parameters are necessary to deploy for this template:

:

.. code-block:: pycon
 
        >>> rhel_templates['101-vm-simple-rhel'].parameters()
        adminPassword
        adminUsername
        vmName

These three parameters need to be set before deploying the template and we will
find out how to set parameters using Simple Azure later in this page.

This information is from ``azuredeploy.parameters.json`` and returned by Pandas
Series:

::


        [template object].parameters()          # pandas Series


Resources
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

According to the metadata earlier, we know that ``101-vm-simple-rhel`` deploys
a virtual machine with Standard D1 but it isn't clear what resources are used.

:

.. code-block:: pycon

        >>> rhel_templates['101-vm-simple-rhel'].resources()
        Microsoft.Compute/virtualMachines      {u'name': u'[parameters('vmName')]', u'apiVers...
        Microsoft.Network/networkInterfaces    {u'name': u'[variables('nicName')]', u'apiVers...
        Microsoft.Network/publicIPAddresses    {u'properties': {u'publicIPAllocationMethod': ...
        Microsoft.Network/virtualNetworks      {u'properties': {u'subnets': [{u'name': u"[var...
        Microsoft.Storage/storageAccounts      {u'properties': {u'accountType': u'[variables(...

There are five services (including ``virtualMachines`` in Compute service) are
described in the template to deploy RHEL image on Microsoft Azure.

This information is from ``azuredeploy.json`` and returned by Pandas Series:

::


        [template object].resources()           # pandas Series


Service Dependency
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Services can be related to other services when it deploys, for example,
``publicIPAddresses`` and ``virtualNetworks`` services are depended on
``networkInterfaces`` resource in the ``101-vm-simple-rhel`` template.
Dependencies are not visible in ``resources()`` but in ``dependson()`` which
returns its relation in python dict data type using pprint():

:

.. code-block:: pycon

        >>> rhel_templates['101-vm-simple-rhel'].dependson_print()
        {u'Microsoft.Compute/virtualMachines': {u'Microsoft.Network/networkInterfaces': {u'Microsoft.Network/publicIPAddresses': {u"[concat(uniquestring(parameters('vmName')), 'publicip')]": {}},
                                                                                         u'Microsoft.Network/virtualNetworks': {u"[concat(uniquestring(parameters('vmName')), 'vnet')]": {}}},
                                                                                                                                 u'Microsoft.Storage/storageAccounts': {u"[concat(uniquestring(parameters('vmName')), 'storage')]": {}}}}


.. note:: `ARMVIZ.io <armviz.io>`_ depicts the service dependency on the web
        like Simple Azure.  For example, ``101-vm-simple-rhel``'s dependency is
        displayed `here
        <http://armviz.io/#/?load=https://raw.githubusercontent.com/Azure/azure-quickstart-templates/master/101-vm-simple-rhel/azuredeploy.json>`_

This information is from ``dependsOn`` section in ``azuredeploy.json`` and
returned by Python dictionary or printed in the Pretty Print (pprint):

::

        [template object].dependson()           # dict type return
        [template object].dependson_print()     # pprint 

Template Deployment
-------------------------------------------------------------------------------

.. tip:: Basic template deployment on Simple Azure is available, see
        :ref:`ref-saz-template-deploy`

Simple Azure has a sub module for Azure Resource Manager (ARM) which deploys a
template on Azure.

:

.. code-block:: pycon

        >>> from simpleazure import arm
        >>> arm = arm.ARM() # Azure Resource Manager object

Next step is loading a template with a parameter.

Load Template        
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*arm* object needs to know which template will be used to deploy and we tell:

:

.. code-block:: pycon

        >>> arm.load_template(rhel['101-vm-simple-rhel'])

Set Parameter
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In our example of RHEL, three parameters need to be set before its deployment,
``adminPassword``, ``adminUsername`` and ``vmName``:

:

.. code-block:: pycon

        >>> arm.set_parameters(
                       {"adminPassword":"xxxxx",
                        "adminUsername":"azureuser",
                        "vmName":"simpleazure-quickstart"}
                      )

        {'adminPassword': {'value': 'xxxxx'},
         'adminUsername': {'value': 'azureuser'},
         'vmName': {'value': 'saz-quickstart'}}

Python dict data type has updated with *value* key name like ``{ '[parameter
name]' : { 'value': '[parameter value'] }}`` and these parameter settings will
be used when the template is deployed.

.. note:: Use ``add_parameter()``, if you have additional parameter to add in
        existing parameters, e.g. add_parameter({"dnsName":"azure-preview"})

Deployment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``deploy()`` function runs a template with a parameter if they are already set.

:

.. code-block:: pycon

        >>> arm.deploy()

Or you can directly deploy a template with parameters.

:

.. code-block:: pycon

        >>> arm.deploy(rhel['101-vm-simple-rhel'], {"adminPassword":"xxxxx", "adminUsername":"azureuser", "vmName":"saz-quickstart"})

It may take a few minutes to complete a deployment and give access to a virtual
machine.

Access
-------------------------------------------------------------------------------

If a template is deployed with an access to virtual machines i.e. SSH via
public IP addresses, ``view_info()`` returns an ip address in a same resource
group. ``Microsoft.Network/PublicIPAddresses`` service is fetched in this
example.

:

.. code-block:: pycon

        >>> arm.view_info()
        [u'40.77.103.150']


Use the same login user name and password from the parameters defined earlier:

:

.. code-block:: console
  
        $ ssh 40.77.103.150 -l azureuser
          The authenticity of host '40.77.103.150 (40.77.103.150)' can't be established.
          ECDSA key fingerprint is 64:fc:dd:7c:98:8c:ed:93:63:61:56:31:81:ad:cf:69.
          Are you sure you want to continue connecting (yes/no)? yes
          Warning: Permanently added '40.77.103.150' (ECDSA) to the list of known hosts.
          azureuser@40.77.103.150's password:
          [azureuser@simpleazure-quickstart-rhel ~]$ 


We confirm that the virutual machine is RHEL 7.2 by:          

.. code-block:: console

          [azureuser@simpleazure-quickstart-rhel ~]$ cat /etc/redhat-release
          Red Hat Enterprise Linux Server release 7.2 (Maipo)

Termination
--------------------------------------------------------------------------------

Deleting a resource group where deployment is made terminates all
services in the resource group.

:

.. code-block:: pycon

        >>> arm.remove_resource_group()


.. comments::

        additional Features
        -------------------------------------------------------------------------------
        - support custom
        - search by technologies, resources, image e.g. Ubuntu, Centos, 
        - preview by replacing variables, parameters
        - elapsed time
        - ease writing new template?
