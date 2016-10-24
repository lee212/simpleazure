# -*- coding: utf-8 -*-

"""
simpleazure.asm.ASM
~~~~~~~~~~~~~~~~~~~~~~~~

This module provides a classic Python library for Windows Azure Virtual
Machines.

 :copyright: 2016, Hyungro Lee (hroe.lee@gmail.com)
 :license: GPLv3

"""

import os
import base64
import random
import copy
from urlparse import urlparse
from time import sleep
from azure import *
from azure import servicemanagement as asm
from .ext.credentials import Credentials
from . import config
from . import ssh
from os.path import expanduser
from .utils import generate_password

class AzureServiceManagement(object):
    """Constructs a :class:`SimpleAzure <SimpleAzure>`.
    Returns :class:`SimpleAzure <SimpleAzure>` instance.

    Usage::

        >>> from simpleazure.asm import ASM as asm
        >>> azure_asm = asm()
        >>> azure_asm.get_config() # Load credentials
        >>> azure_asm.create_vm()
        <azure.servicemanagement.AsynchronousOperationResult at 0x2945e10>
    """

    subscription_id = ""
    certificate_path = ""

    #ServiceManagementService
    sms = None

    #default value
    name = "sazvm-12345"
    location = "East US"

    cluster_name_prefix = "sazvm-cluster-"

    image = None
    image_name = ""
    _image_name = { "os" : "Linux",
                   "category" : "Canonical",
                   "label" : "12.04" }
    os_name = None

    # Storage
    storage_account = ""
    container = "os-image"
    blob = ""
    blob_ext = ".vhd"
    windows_blob_url = "blob.core.windows.net"
    media_link = ""

    # Linux
    linux_user_id = 'azureuser'
    linux_user_passwd = 'mypassword1234@' #Not used in ssh

    #SSH Keys
    # http://msdn.microsoft.com/en-us/library/windowsazure/jj157194.aspx#SSH
    azure_config = config.azure_path()
    thumbprint_path = azure_config + '/.ssh/thumbprint'
    authorized_keys = "/home/" + linux_user_id + "/.ssh/authorized_keys"
    public_key_path = expanduser("~") + "/.ssh/id_rsa.pub" # rsa public key
    private_key_path = azure_config + '/.ssh/myPrivateKey.key'
    key_pair_path = private_key_path
    ssh_key_is_on = False

    #Adding for cluster
    num_4_win = 0
    num_4_lin = 4
    cluster_count = num_4_win + num_4_lin

    def __init__(self):
        """Initialize variables"""
        self.set_name()
        self.set_location()
        self.set_role_size()
        self.get_config()

    def set_name(self, name=None):
        """Set a name of virtual machine. If name is not specified, random name
        will be generated in form of 'sazvm-' following with five digits.
        
        :param name: the name to use for a virtual machine
        :type name: str.

        """
        if not name:
            name = 'sazvm-' + self.get_random()
        self.name = name

    def get_name(self):
        """Return a name of the virtual machine.

        :returns: str

        """
        return self.name
        
    def get_random(self):
        """Return a random string in a five digits.

        :returns: str

        """
        return ''.join(str(x) for x in random.sample(range(0,10), 5))

    def set_location(self, location=config.DEFAULT_LOCATION):
        """Set a location for the virtual machine among available locations.

        :param location: the name of a location to use
        :type location: str.

        """

        # TODO 'display_name' is being used like 'Central US' instead of its name 'centralus'
        # ARM mode uses its name 'centralus', we need to check ASM still works with the name
        self.location = location

    def get_location(self):
        return self.location

    def set_role_size(self, size=config.DEFAULT_ROLE_SIZE):
        """Set a role (flavor) size for the virtual machine among ExtraSmall, Small,
        Medium, Large, ExtraLarge

        :param size: the name of a role size to create
        :type size: str.

        ref:
        http://msdn.microsoft.com/en-us/library/windowsazure/jj157194.aspx#bk_role

        """
        self.role_size = size

    def get_role_size(self):
        """Return a role size of the virtual machine.

        "returns: str

        """
        return self.role_size

    def get_config(self):
        """Load configurations for the virtual machine. For example, credentials
        should be loaded to connect Windows Azure Services."""

        self.get_creds()

    def get_creds(self):
        """Load credentials such as a subscription_id and a certificate path in
        a local system. These information should be set by the azure-cli
        tool."""
        self.cert = Credentials()
        self.subscription_id = self.cert.getSubscriptionId()
        self.certificate_path = self.cert.getManagementCertFile()

    def create_vm(self, name=None, location=None):
        """Create a Window Azure Virtual Machine

        :param name: (optional) the name of a virtual machine to use.
        :type name: str.
        :param location: (optional) the name of a location to use for the
        virtual machine.
        :type location: str.
        :returns: azure.servicemanagement.AsynchronousOperationResult

        """
        self.set_name(name)
        self.connect_service()
        self.create_cloud_service(name, location)
        self.set_image()
        self.get_media_link(blobname=name)

	self.linux_user_passwd = generate_password(16)
        os_hd = asm.OSVirtualHardDisk(self.image_name, self.media_link)
        linux_config = asm.LinuxConfigurationSet(self.get_name(),
                self.linux_user_id, self.linux_user_passwd, self.ssh_key_is_on)

        self.set_ssh_keys(linux_config)
        self.set_network()
        self.set_service_certs()
        # can't find certificate right away.
        sleep(5)

        result = \
        self.sms.create_virtual_machine_deployment(service_name=self.get_name(),\
        deployment_name=self.get_name(), deployment_slot='production',\
        label=self.get_name(), role_name=self.get_name(), \
        system_config=linux_config, os_virtual_hard_disk=os_hd, \
        network_config=self.network, role_size=self.get_role_size())

        self.result = result
        return result

    def get_login_info(self):
        """return SSH id/pass"""
        return {"id":self.linux_user_id, "pass":self.linux_user_passwd}

    def connect_service(self, refresh=False):
        """Connect Windows Azure Service via ServiceManagementService() with a
        subscription id and a certificate. 
        
        :param refesh: (optional) the connection will be update if refresh is
        set
        :type refresh: bool.
        
        """
        if not hasattr(self, 'cert'):
            self.get_creds()
        if not self.sms or refresh:
            self.sms = asm.ServiceManagementService(self.subscription_id,
                    self.certificate_path)

    def create_cloud_service(self, name=None, location=None):
        """Create a cloud (hosted) service via create_hosted_service()

        :param name: (optional) the name of a cloud service to use
        :type name: str.
        :param location: (optional) the name of a location for the cloud service 
        :type location: str.

        """
        if not name:
            name = self.get_name()
        if not location:
            location = self.location
        self.sms.create_hosted_service(service_name=name, label=name,
                location=location)

    def use_ssh_key(self, yn=False):
        """Enable SSH Key to connect"""
        self.ssh_key_is_on = yn

    def set_ssh_keys(self, config):
        """Configure login credentials with ssh keys for the virtual machine.
        This is only for linux OS, not Windows.

        :param config: the return value of LinuxConfigurationSet()
        :type config: class LinuxConfigurationSet

        """

	if not self.ssh_key_is_on:
            return
        # fingerprint captured by 'openssl x509 -in myCert.pem -fingerprint
        # -noout|cut -d"=" -f2|sed 's/://g'> thumbprint'
        # (Sample output) C453D10B808245E0730CD023E88C5EB8A785ED6B
        self.thumbprint = open(self.thumbprint_path,
                'r').readline().split('\n')[0]
        publickey = asm.PublicKey(self.thumbprint, self.public_key_path)
        # KeyPair is a SSH kay pair both a public and a private key to be stored
        # on the virtual machine.
        # http://msdn.microsoft.com/en-us/library/windowsazure/jj157194.aspx#SSH
        keypair = asm.KeyPair(self.thumbprint, self.key_pair_path)
        config.ssh.public_keys.public_keys.append(publickey)
        config.ssh.key_pairs.key_pairs.append(keypair)

        # Note
        # Since PKCS#10 X.509 is not fully supported by pycrypto, paramiko can
        # not use the key generated with PKCS, for example, openssl req ...
        # To do bypass, ssh-keygen can be used in the following order
        #
        # Generate a key pair
        # 1. ssh-keygen -f myPrivateKey.key (default is rsa and 2048 bits)
        #
        # Get certificate from a private key
        # 2. openssl req -x509 -nodes -days 365 -new -key myPrivateKey.key
        # -out myCert.pem
        #
        # .cer can be generated
        # openssl x509 -outform der -in public_key_file.pem -out myCert.cer
        #
        # .pfx
        # openssl pkcs12 -in public_key_file.pem -inkey private_key_file.key
        # -export -out myCert.pfx

        # Reference:
        # http://www.sslshopper.com/article-most-common-openssl-commands.html

    def set_network(self):
        """Configure network for a virtual machine.
        End Points (ports) can be opened through this function.
        For example, opening ssh(22) port will be configured.

        """
        network = asm.ConfigurationSet()
        network.configuration_set_type = 'NetworkConfiguration'
        network.input_endpoints.input_endpoints.append(asm.ConfigurationSetInputEndpoint('ssh',
            'tcp', '22', '22'))
        self.network = network

    def set_service_certs(self):
        """Add a certificate to cloud (hosted) service.
        Personal Information Exchange (.pfx) should exist in the azure config
        directory (e.g. $HOME/.azure/.ssh/myCert.pfx). Python SDK only support
        .pfx at this time.

        """
        if not self.ssh_key_is_on:
            return
        # command used: 
        # openssl pkcs12 -in myCert.pem -inkey myPrivateKey.key
        # -export -out myCert.pfx
        cert_data_path = self.azure_config + "/.ssh/myCert.pfx"
        with open(cert_data_path, "rb") as bfile:
            cert_data = base64.b64encode(bfile.read())

        cert_format = 'pfx'
        cert_password = ''
        cert_res = self.sms.add_service_certificate(service_name=self.get_name(),
                                                    data=cert_data,
                                                    certificate_format=cert_format,
                                                    password=cert_password)
        self.cert_return = cert_res

    def list_images(self):
        """List available operating systems images on Windows Azure.

        :returns: dict.

        """
        return self.get_registered_image()

    def get_registered_image(self, label=None, name=None):
        """Return available operating systems images on Windows Azure

        :param label: (optional) a simple description of images. not unique
        value
        :type label: str.
        :param name: (optional) a unique name of images.
        :type name: str.
        :returns: dict.

        """

        # Establish connection, if not exist
        self.connect_service()
        images = self.sms.list_os_images()
        if not label and not name:
            return images

	lastone = None
        for image in images:
            if name and image.name == name:
                return image
            if label and image.label == label:
                lastone = image

        if lastone:
            return lastone

        return images

    def list_storage_accounts(self):
        """List available storage accounts for the subscription id.

        :returns: dict.

        """
        self.connect_service()
        return self.sms.list_storage_accounts()

    def get_status(self, request_id=None):
        """Return a status of a deployed virtual machine with a request id.

        :param request_id: (optional) a request id to look up.
        :type request_id: str.
        :returns: dict.

        """
        if not request_id:
            request_id = self.result.request_id
        self.connect_service()
        return self.sms.get_operation_status(request_id)

    def get_deployment(self):
        """Return a detailed information of a deployment with the name.

        :returns: dict.

        """
        self.connect_service()
        return self.sms.get_deployment_by_name(service_name=self.get_name(),
                                               deployment_name=self.get_name())

    def list_deployments(self):
        """Return a list of deployments

        :returns: dict.

        """
        self.connect_service()
        return self.sms.list_hosted_services()

    def delete_vm(self, name=None):
        """Delete vm instance"""

        res = self.sms.delete_deployment(name or self.get_name(), name or
                self.get_name(), delete_vhd=True)
        return res

    def set_image(self, name=None, image=None, refresh=False):
        """Set os image to deploy virtual machines.
        self.image_name and self.os_name will be set

        :param name: (optional) an image name to set
        :type name: str.
        :param image: (optional) an oject of an image
        :type image: obj. (azure.servicemanagement.OSImage) 
        :param refresh: (optional) reset an image name
        :type refresh: bool.

        """
        # if set then skip unless it's forced.
        if self.image_name and not refresh:
            return

        #get a default image
        if not name and not image:
            image = self.get_registered_image(label=config.DEFAULT_IMAGE_LABEL)

        # set image
        if image:
            self.image = image
            self.image_name = image.name
            self.os_name = image.os

    def get_media_link(self, storage_account=None, container=None, blobname=None):
        """Return a media link in http URL.
        
        :param storage_account: (optional) a name of a storage account to use.
        :type storage_account: str.
        :param container: (optional) a name of a container to use.
        :type container: str.
        :param blobname: (optional) a name of a blob file to use.
        :type blobname: str.
        :returns: str
        
        """
        if not storage_account:
            storage_account = self.get_storage_account()
        if not blobname:
            blobname = self.get_name()
        if not container:
            container = self.container
        blob_prefix = self.os_name
        blob = blob_prefix + "-" + blobname + self.blob_ext
        media_link = "http://" + storage_account + "." + self.windows_blob_url \
                + "/" + container + "/" + blob
        self.media_link = media_link
        return media_link

    def get_storage_account(self, refresh=False):
        """Return a storage account.

        If there is a selected image to deploy, the same storage account will be
        used with the image's one.
        Otherwise, the last storage account of a subscription id will be used.

        Note. 
        The disk's VHD must be in the same account as the VHD of the source
        image (source account: xxx.blob.core.windows.net, target
        account: xxx.blob.core.windows.net).

        """

        if self.image and self.image.media_link:
            account_name = self.get_account_from_link(self.image.media_link)
        else:
            account_name = self.get_last_storage_account()
        
        self.storage_account = account_name
        return account_name

    def get_last_storage_account(self, refresh=False):
        """Return the last storage account name of a subscription id
 
        :param refesh: (optional) the storage account name will be update if
        refresh is set
        :type refresh: bool.
        :returns: str.

        """
        self.connect_service()
        if not self.storage_account or refresh:
            result = self.sms.list_storage_accounts()
            for account in result:
                storage_account = account.service_name
        try:
            return storage_account
        except:
            storage_account = self.create_storage_account()
            #storage_account = self.get_name()
            return storage_account

    def create_storage_account(self):
        name = self.get_name()[:24].replace("-","")
        description = name + "description"
        label = name + "label"
        self.sms.create_storage_account(service_name=name,
                                        description=description, label=label,
                                        location=self.get_location())
        self.storage_name = name
        return name

    def get_account_from_link(self, url):
        """Return hostname from a link.
        top hostname indicates a storage account name

        :param url: a media_link
        :type url: str.

        """
        try:
            o = urlparse(url)
            host = o.hostname.split(".")[0]
        except:
            host = None

        return host
        
    def create_cluster(self, num=None, option=None):
        """Create multiple virtual machines to support cluster computing
        
        :param num: (optional) the number of virtual machines to create. Default
        is 4.
        :type num: int.
        :param option: (optional) the detailed information for cluster nodes to
        create.
        :type option: dict.
        :returns: list.

        """

        cluster_count = num
        if not num:
            cluster_count = self.cluster_count
        #results = []
        results = {}
        # It is supposed to use multi-processing instead of for loop
        for cnt in range(cluster_count):
            self.set_name(self.cluster_name_prefix + str(cnt) + "-" +
                    self.get_random())
            result = self.create_vm(self.get_name())
            sleep(15)
            #results.append(result)
            results[self.get_name()] = result
            if cnt == 0:
                results["master"] = self.get_name()

            #media_link = self.get_media_link(blobname=new_name)
            #self.create_cloud_service(name=new_name)
            #temporarily added waiting time for deploying cloud service
        self.results = results
        return results

    def login_to(self, name=None, login_id=None, passwd=None, ssh_key=None):
        """SSH to a virtual machine
        
        :param name: (optional) the hostname of a virtual machine
        :type name: str.
        :returns: ssh object.
        
        """

        if not name:
            name = self.name
        hostname = config.get_azure_domain(name)

        sshmaster = ssh.SSH()
        self.sshmaster = sshmaster
        if ssh_key:
            sshmaster.setup(host_string = hostname, key_filename = ssh_key or
                    self.private_key_path)
        else:
            sshmaster.setup(host_string = hostname, user = login_id or
                    self.linux_user_id, password = passwd or
                    self.linux_user_passwd)
        sshmaster.shell()

    def get_username(self):
        return self.linux_user_id

    def get_pkey(self):
        return self.private_key_path

    def purge_all(self):
        """Delete all resources"""

        res=None
        self.connect_service()
        # Delete hosted services
        hosted_services = self.sms.list_hosted_services()
        for i in hosted_services:
            svc_props = self.sms.get_hosted_service_properties(i.service_name,
                    True)
            for j in svc_props.deployments:
                self.delete_vm(j.name) #i.service_name)
            # log("{0} (vm) deletion requested".format(i.service_name))
            try:
                res = self.sms.delete_hosted_service(i.service_name)
            except:
                print ("Failed to delete {0}".format(i.service_name))
                pass
            # log("{0} (cloud service) deletion requested".format(i.service_name))

        # delete disks
        disks = self.sms.list_disks().disks
        for i in disks:
            try:
                res = self.sms.delete_disk(i.name)
            except:
                print ("Failed to delete {0}".format(i.name))
                pass
        # Delete storage account
        storage = self.sms.list_storage_accounts()
        for i in storage:
            try:
                res = self.sms.delete_storage_account(i.service_name)
                # log("{0} (storage) deletion requested".format(i.service_name))
            except:
                print ("Failed to delete {0}".format(i.service_name))
                pass

    def get_all_items(self):
        self.connect_service()
        all_items = {}

        # The following items are displayed:
        # - cloud services
        # - storage
        # - virtual machines


        supported = ['hosted_services', 'deployments', 'storage']
        item = { 'count': 0, 'names': [] }

        # initialize
        for i in supported:
            # shallow, deep copy - reference or value copy of inside objects
            all_items[i] = copy.deepcopy(item)
        
        # hosted services, deployments
        hosted_services = self.sms.list_hosted_services()
        all_items['hosted_services']['count'] = len(hosted_services)
        for i in hosted_services:
            svc_props = self.sms.get_hosted_service_properties(i.service_name,
                    True)
            all_items['deployments']['count'] += len(svc_props.deployments)
            for j in svc_props.deployments:
                all_items['deployments']['names'].append(j.name)
            all_items['hosted_services']['names'].append(i.service_name)

        storage = self.sms.list_storage_accounts()
        all_items['storage']['count'] = len(storage)
        for i in storage:
            all_items['storage']['names'].append(i.service_name)
        return all_items

# Tips
# 
# 'hosted_service'
# returns like:
#
# {'url': u'https://management.core.windows.net/6b3cf2b5-2cc1-4828-b5e0-9f8be72e6e6f/services/hostedservices/sazvm-16203', 'service_name': u'sazvm-16203', 'hosted_service_properties': <azure.servicemanagement.models.HostedServiceProperties object at 0x7f9557815e90>, 'deployments': None}

