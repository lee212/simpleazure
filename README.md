Simple Azure
===============================================================================

Simple Azure supports cloud computing management in the Python Programming Language. It plans to support WIndows Azure, OpenStack, etc.  
[Documentation](https://simple-azure.readthedocs.org/)

Prerequisite
-------------------------------------------------------------------------------

- Azure Cli installation

```
    sudo apt-get install nodejs-legacy
    sudo apt-get install npm
    sudo npm install -g azure-cli
```

Account Setup
-------------------------------------------------------------------------------

- Open a browser to http://go.microsoft.com/fwlink/?LinkId=254432
- ``*-DD-MM-YYYY-credentials.publishsettings`` is downloaded on a local directory
- Run ``azure config mode as`` # To run azure cli tool via the classic service management certificate.
- Run ``azure account import <publishsettings file>``
- Run ``azure account cert export ~/.azure/managementCertificate.pem``

Example
-------------------------------------------------------------------------------
Create a VM on Windows Azure
(ubuntu 14.04 is a default image)

```
from simpleazure.simpleazure import SimpleAzure as saz

azure = saz()
azure.get_config()
azure.create_vm()
```

Status can be seen here.
```
print vars(azure.get_status())
{'error': None, 'http_status_code': u'200', 'id': u'', 'status': u'Succeeded'}
```
or
```
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
 ```

Example for multiple deployment
-------------------------------------------------------------------------------
cluster() function helps to deploy several VMs at once.

```
azure = saz()
azure.get_config()
azure.create_cluster()
```

```
my-cluster-vm-0-87412
{'request_id': '88c94c00288d42acaf877783f09c4558'}
my-cluster-vm-1-61293
{'request_id': 'abfd563c2c4f4926872b6b1dba27a93b'}
my-cluster-vm-2-96085
{'request_id': '29b55f6cb5e94cfdbf244a7c848c854d'}
my-cluster-vm-3-46927
{'request_id': 'b1a3446ebafe47a295df4c9d1b7d743c'}
```

Example for multiple deployment with Azure Data Science Core
-------------------------------------------------------------------------------
Deploy 5 VMs with Azure Data Science Core at West Europe 

```
azure = saz()
azure.get_config()
q = azure.get_registered_image(name="Azure-Data-Science-Core")
azure.set_image(image=q,refresh=True)
azure.set_location("West Europe")
azure.create_cluster(num=5)
```

List of VMs
-------------------------------------------------------------------------------

```
vars(azure.list_deployments().hosted_services)
```

Terminating VM
-------------------------------------------------------------------------------

```
azure.delete_vm()
```

or

```
azure.delete_vm('vm-name')
```

Clustering
-------------------------------------------------------------------------------

TBD

Description
-------------------------------------------------------------------------------
* This development is planned to support ipython clustering modules/plugines like the StarCluster project (which is supporting Amazon EC2).
* This development is planned to support command-line tools to launch / execute .ipynb files in parallel.

Contact
-------------------------------------------------------------------------------

hroe.lee at gmail.com
