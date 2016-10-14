Deploying Azure QuickStart Templates
===============================================================================

Azure provides 407 community templates[1]_  from starting a single virtual
instance to hadoop clusters with Apache Spark and Simple Azure supports
deploying these templates in Python with its (directory) name.
.. comment:: to ease service and infrastructure deployments on Microsoft Azure.

::

        >> from simpleazure.azure_quickstart_templates import AzureQuickStart as aqst
        >> template = aqst.get_template('101-vm-sshkey')
        >> template.metadata()
        dateUpdated                                               2015-06-05
        description        This template allows you to create a Virtual M...
        githubUsername                                             squillace
        itemDisplayName     Deploy a Virtual Machine with SSH rsa public key
        summary             Deploy a Virtual Machine with SSH rsa public key

The example above imports ``101-vm-sshkey`` template and ``metadata()`` returns
its description which is about deploying a single Ubuntu VM with a ssh key for
access. You can find a template name i.e. 101-vm-sshkey from the github
repository [2]_ where each template is served in a single directory with
required files i.e. azuredeploy.json, azuredeploy.parameters.json, and
metadata.json. ``get_templates()`` returns all templates therefore other
templates are fetched and ready to deploy. For example:

::

        >> templates = aqst.get_templates()
        >> templates.ten()
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

Details for a template are also available like metadata (from metadata.json):

::
        >>> templates['101-acs-dcos'].metadata()
        dateUpdated                                               2016-02-18
        description        Deploy an Azure Container Service instance for...
        githubUsername                                              rgardler
        itemDisplayName                      Azure Container Service - DC/OS
        summary            Azure Container Service optimizes the configur...



        >> from simpleazure import arm
        >> from simpleazure.azure_quickstart_templates import AzureQuickStart as aqst
        >> arm = arm.ARM() # Azure Resource Manager object
        >> aqst = aqst.AzureQuickStartTemplate()
        >> vm_sshkey_template = aqst.get_template('101-vm-sshkey')
        >> vm_sshkey_template.requirements()
        {u'sshKeyData': u'GEN-SSH-PUB-KEY'}
        >> arm.set_parameter("sshKeyData", "ssh-rsa AAAB... hrlee@quickstart")

.. comment::
        - statistics for deploying time, number of resources, price tags, options, limitations (versions, os distribution)
          - possible more information of sizes, image,
        - statistics for technologies
        - sub templates (probably supported?) 
        - 407  as of october 2016

.. [1] as of 10/13/2016 from https://github.com/Azure/azure-quickstart-templates
.. [2] https://github.com/Azure/azure-quickstart-templates

Searching Template
-------------------------------------------------------------------------------

Simple Azure supports template search with a keyword from the Azure QuickStart
Templates. Let's find templates that use 'rhel' (Red Hat Enterprise Linux) in a
description. It found 13 templates and the first ten items are like: 

::

        >> rhel_templates = aqst.search("rhel")
        >> len(rhel_templates)
        13
        >> rhel_templates.ten()
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

See metadata of the second templates ``101-vm-simple-rhel``:

::

        >> rhel_templates['101-vm-simple-rhel'].metadata()
        dateUpdated                                               2016-02-23
        description        This template will deploy a Red Hat Enterprise...
        githubUsername                                            BorisB2015
        itemDisplayName    Red Hat Enterprise Linux VM (RHEL 7.2 or RHEL ...
        summary            This template will deploy RedHat (RHEL) VM, us...

It requires these parameters:

::
 
        >>> rhel_templates['101-vm-simple-rhel'].parameters()
        adminPassword
        adminUsername
        vmName


Simple Azure Features
-------------------------------------------------------------------------------
- support official azure quickstart templates (407 avail)
- support custom
- search by technologies, resources, image e.g. Ubuntu, Centos, 
- preview by replacing variables, parameters
- elapsed time
- visualization?
- ease writing new template?
