Installation
=============
You could install Simple Azure via pypi or github.
You need Python 2.7+ and Python 3.0+ is not supported.

Prerequisite
--------------
Simple Azure is based on azure-sdk-for-python which is a python library for Windows Azure Management. 

* azure-sdk-for-python
* azure-cli

Virtualenv and virtualenvwrapper
-----------------------------------
Virtualenv enables project-based development for python and virtualenvwrapper provides simple commands to switch different python environments.
It is not required to install but may be helpful especially when you don't have a super-user privilege.


Pypi with virtualenv
--------------------
::
  
  $ mkvirtualenv simpleazure
  (simpleazure)$ pip install simpleazure
  
pypi - system wide installation with sudo
-----------------------------------------
::

  $ sudo pip install simpleazure
  

github
-------
::

   $ git clone https://github.com/lee212/simpleazure.git
   
pypi on Windows
------------------------------
On Windows, *easy_install* help install Simple Azure. `distribute_setup.py <http://python-distribute.org/distribute_setup.py>`_ file do an installation of easy_install.

.. Next, add the easy_install command and other Python scripts to the command search path, by adding your Python installation’s Scripts folder to the PATH environment variable. To do that, right-click on the “Computer” icon on the Desktop or in the Start menu, and choose “Properties”. Then click on “Advanced System settings” (in Windows XP, click on the “Advanced” tab instead). Then click on the “Environment variables” button. Finally, double-click on the “Path” variable in the “System variables” section, and add the path of your Python interpreter’s Scripts folder. Be sure to delimit it from existing values with a semicolon. Assuming you are using Python 2.7 on the default path, add the following value:

``;C:\Python27\Scripts``

.. And you are done! To check that it worked, open the Command Prompt and execute easy_install. If you have User Account Control enabled on Windows Vista or Windows 7, it should prompt you for administrator privileges.

Once you have easy_install, you can install simple azure:

:: 

  > easy_install pip
  > pip install simpleazure

