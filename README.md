Simple Azure
============

Simple Azure supports cloud computing management in the Python Programming Language. It plans to support WIndows Azure, OpenStack, etc.

Example
--------
Create a VM on Windows Azure
(ubuntu 12.04 is a default image)

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
 
Example #1 (TBD)
----------------
```
from simpleazure.simpleazure import simpleazure as saz

def square(x):
    return x*x

c = saz()
res = c.call(square, 3) # square(3) evaluated on the cloud (Azure, OpenStack, etc)

print res # 9
```

The Simple Azure with ipython notebook (TBD)
--------------------------------------------
The simple JSON typed ipython notebook file (*.ipynb) can be easily shared and can be found at http://nbviewer.ipython.org/.
We can probably provide a simple command line tools to execute the notebook files on Azure like StarCluster.

Example #2 (TBD)
----------
```
$ simpleazure start -n 4 azure.ipynb

or

$ simpleazure start -n 4 http://raw.github.com/lee212/simpleazure/gh-pages/azure.ipynb
```

Description
-----------
* This development is planned to support ipython clustering modules/plugines like the StarCluster project (which is supporting Amazon EC2).
* This development is planned to support command-line tools to launch / execute .ipynb files in parallel.
