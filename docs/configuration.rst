Configuration (classic mode)
===============================================================================

Simple Azure uses the default directory for the azure-cli tool,
``$HOME/.azure``.  It contains the ``config.json`` which includes an endpoint
and a subscription of Windows Azure.

SSH Keys
-------------------------------------------------------------------------------

``.ssh`` directory contains certificates and thumbprints (fingerprints) of key
pairs on the default directory ``$HOME/.azure``.

pfx certificate
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Personal Information Exchange (pfx) certificate is required to the Cloud
(hosted) service.

``openssl`` supports to convert your public and private keys to a pfx
certificate.

private key files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
For example, ``myPrivateKey.key`` which is a rsa 2048 private key is used to
get access to virtual machines using SSH.

Cluster configuration
-------------------------------------------------------------------------------

Simple Azure supports cluster computing and personal profiles enable individual
settings when you launch clusters.  The default directory for cluster conf file
is ``cluster`` under the ``$HOME/.azure`` default directory.

Cluster profile
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For example, ``mycluster`` has information in a yaml format in the cluster
directory.

::

  master: myvm-81fd6840ae
  engines: [myvm-4406510ce8,myvm-7103520de1,myvm-5103520de4,myvm-5104120de1]
  pkey: /home/azureuser/.azure/.ssh/myPrivateKey.key
  num: 5
