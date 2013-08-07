Command
===============

Simple Azure supports command line tools, so a user can create virtual machines on the shell.

Creating Clusters
------------------

simpleazure-cluster
^^^^^^^^^^^^^^^^^^^^^
A user can create one or more clusters of virtual machines on Windows Azure:

::

   $ simpleazure-cluster start mycluster

Note. ``mycluster`` is a profile name and the config file has been stored under the default directory ``$HOME/.azure/cluster`` as a yaml file.

The number of clusters can be changed in the config file (mycluster.yaml) like this:

::

    ...
    num=5
