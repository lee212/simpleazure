Quickstart
============

This page provides a good introduction to Simple Azure.

Deploying Azure Virtual Machine
--------------------------------

.. code-block:: python

   from simpleazure.simpleazure import SimpleAzure as saz

   azure = saz()
   azure.get_config()
   azure.create_vm()
   
You can change an operating system image by the ``set_image()`` function. For example, *Ubuntu 12.04 distribution* can be selected like as follows:

.. code-block:: python

   azure.set_image(label="azure.Ubuntu Server 12.04.2 LTS")

This allows you to create a vm with the selected image. Note that ``set_image()`` must be set before calling the ``create_vm()`` function.
