
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
