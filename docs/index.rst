.. Simple Azure documentation master file, created by
   sphinx-quickstart on Tue Aug  6 22:36:05 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Simple Azure - Python library for Windows Azure
================================================

Simple Azure is a python library for Windows Azure. 
It provides a service management with clustering. 
Simple Azure enables ipython notebook on Windows Azure based on the azure-sdk-for-python and its plugin. 
Linux distributions on VM Depot are accessible with the Azure node.js SDK. 
IPython cluster is also supported.

* cluster computing (like StarCluster)
* IPython cluster with the plugin
* Access to the open VM image repository (VM Depot)

You can get started with :doc:`Quickstart </quickstart>` and then learn more through :doc:`Tutorial </tutorial>` that shows how to deploy and utilize Windows Azure with Simple Azure.
:doc:`Installation </installation>` and :doc:`Configuration </configuration>` helps you get Simple Azure installed on your machine and :doc:`Command </command>` describes how to use Simple Azure on the shell.
You can find resources :doc:`here </deliverables>`.

Deploying Azure Virtual Machines
---------------------------------
Three lines are required to deploy Window Azure Virtual Machine in Python.

.. code-block:: python

   from simpleazure.simpleazure import SimpleAzure as saz

   azure = saz()
   azure.get_config()
   azure.create_vm()
   
.. raw:: html

   <iframe width="560" height="315" src="//www.youtube.com/embed/pHG_gmnc6qI" frameborder="0" allowfullscreen></iframe>

Installation (TBD)
------------------

::

  $ pip install simpleazure
  $ simpleazure-cluster start mycluster

Contribute
===========

* Mailinglist
* `issues <https://github.com/lee212/simpleazure/issues>`_


Content
=======

.. toctree::
   :maxdepth: 1

   quickstart
   tutorial
   installation
   command
   configuration
   deliverables
   
Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
