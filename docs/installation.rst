Installation
===============================================================================

Simple Azure Installation is available via github, Pypi and docker image.

.. warning:: Python 3.0+ is not supported.

Docker Installation
-------------------------------------------------------------------------------

Simple Azure is available in a Docker image to run.

- With IPython Notebook:

.. code-block:: console

        docker run -d -p 8888:8888 lee212/simpleazure_with_ipython

Open a browser with the port number **8888**.

- Simple Azure only:

.. code-block:: console

        docker run -i -t lee212/simpleazure

Python Pypi Installation
-------------------------------------------------------------------------------

.. code-block:: console

   pip install simpleazure

Github Installation
-------------------------------------------------------------------------------

.. code-block:: console

   git clone https://github.com/lee212/simpleazure.git
   cd simpleazure
   pip install -r requirements.txt
   python setup.py install

Virtualenv and virtualenvwrapper
-------------------------------------------------------------------------------

Virtualenv enables project-based development for python and virtualenvwrapper
provides simple commands to switch different python environments.  It is not
required to install but would be useful when you need a user space installation
without super-user privilege.


Pypi with virtualenv
-------------------------------------------------------------------------------

::
  
  $ mkvirtualenv simpleazure
  (simpleazure)$ pip install simpleazure
  
pypi - system wide installation with sudo
-------------------------------------------------------------------------------

::

  $ sudo pip install simpleazure
  

pypi on Windows
-------------------------------------------------------------------------------

On Windows, *easy_install* help install Simple Azure. `distribute_setup.py
<http://python-distribute.org/distribute_setup.py>`_ file do an installation of
easy_install.

.. Next, add the easy_install command and other Python scripts to the command search path, by adding your Python installation’s Scripts folder to the PATH environment variable. To do that, right-click on the “Computer” icon on the Desktop or in the Start menu, and choose “Properties”. Then click on “Advanced System settings” (in Windows XP, click on the “Advanced” tab instead). Then click on the “Environment variables” button. Finally, double-click on the “Path” variable in the “System variables” section, and add the path of your Python interpreter’s Scripts folder. Be sure to delimit it from existing values with a semicolon. Assuming you are using Python 2.7 on the default path, add the following value:

``;C:\Python27\Scripts``

.. And you are done! To check that it worked, open the Command Prompt and execute easy_install. If you have User Account Control enabled on Windows Vista or Windows 7, it should prompt you for administrator privileges.

Once you have easy_install, you can install simple azure:

:: 

  > easy_install pip
  > pip install simpleazure

