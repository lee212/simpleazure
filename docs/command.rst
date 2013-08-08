Command
===============

Simple Azure supports command line tools, so a user can create virtual machines on the shell.

Creating Clusters
------------------
The usage is based on StarCluster. We aim to provide an identical interface and command name to use clusters like StarCluster.

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

sshmaster
''''''''''''
This command allows to login to a master node via SSH.

::
  
   $ simpleazure-cluster sshmaster mycluster
   [myvm-81fd6840ae.cloudapp.net] run: bash
   [myvm-81fd6840ae.cloudapp.net] out: azureuser@myvm-81fd6840ae:~$ ls -al
   [myvm-81fd6840ae.cloudapp.net] out: total 52
   [myvm-81fd6840ae.cloudapp.net] out: drwxr-xr-x 6 azureuser azureuser 4096 Jul 29 23:50 .
   [myvm-81fd6840ae.cloudapp.net] out: drwxr-xr-x 3 root      root      4096 Jul 25 22:06 ..
   [myvm-81fd6840ae.cloudapp.net] out: -rw------- 1 azureuser azureuser 4617 Aug  6 21:38 .bash_history
   [myvm-81fd6840ae.cloudapp.net] out: -rw-r--r-- 1 azureuser azureuser  220 Apr  3  2012 .bash_logout
   [myvm-81fd6840ae.cloudapp.net] out: -rw-r--r-- 1 azureuser azureuser 3486 Apr  3  2012 .bashrc
   [myvm-81fd6840ae.cloudapp.net] out: drwx------ 2 azureuser azureuser 4096 Jul 25 22:22 .cache
   [myvm-81fd6840ae.cloudapp.net] out: drwxrwxr-x 4 azureuser azureuser 4096 Jul 27 20:17 .ipython
   [myvm-81fd6840ae.cloudapp.net] out: -rw-r--r-- 1 azureuser azureuser  675 Apr  3  2012 .profile
   [myvm-81fd6840ae.cloudapp.net] out: drwx------ 2 azureuser azureuser 4096 Jul 26 19:22 .ssh
   [myvm-81fd6840ae.cloudapp.net] out: -rw------- 1 azureuser azureuser 5658 Jul 26 22:44 .viminfo
   [myvm-81fd6840ae.cloudapp.net] out: drwx------ 2 azureuser azureuser 4096 Jul 29 23:56 .w3m
   [myvm-81fd6840ae.cloudapp.net] out: azureuser@myvm-81fd6840ae:~$ hostname
   [myvm-81fd6840ae.cloudapp.net] out: myvm-81fd6840ae
   [myvm-81fd6840ae.cloudapp.net] out: azureuser@myvm-81fd6840ae:~$ exit
   [myvm-81fd6840ae.cloudapp.net] out: exit
   [myvm-81fd6840ae.cloudapp.net] out:
