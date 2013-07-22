IPython plugin
==============

The SimpleAzure plans to support ipython parallel module on Windows Azure. It is a simply functionality which StarCluster + Ipython has.

Example
----------
```
from simpleazure.simpleazure import simpleazure as saz
from IPython.parallel import Client

c = Client()

c.ids
# set([0, 1, 2, 3]) means 4 Azure VMs

c[:].apply_sync(lambda : "Hello, World")
```
