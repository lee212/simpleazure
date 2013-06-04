The cloud
==========

The cloud supports cloud computing management in the Python Programming Language. It plans to support WIndows Azure, OpenStack, etc.

Example
-------
```
import thecloud

def square(x):
    return x*x

c = thecloud()
res = c.call(square, 3) # square(3) evaluated on the cloud (Azure, OpenStack, etc)

print res # 9
```

Description
-----------
* This development is planned to support ipython clustering modules/plugines like the StarCluster project (which is supporting Amazon EC2).
* This development is planned to support command-line tools to launch / execute .ipynb files in parallel.
