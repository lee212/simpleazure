import os
import base64
import random
from time import sleep
from azure import *
from azure.servicemanagement import *
from ext.credentials import Credentials

class SimpleAzure:

    config_path = os.environ["HOME"] + "/.azure/"
    subscription_id = ""
    certificate_path = ""

    #ServiceManagementService
    sms = None

    #default value
    name = "myvm-12345"
    location = "Central US"

    image_name = ""
    _image_name = { "os" : "Linux",
                   "category" : "Canonical",
                   "label" : "12.04" }

    # Storage
    storage_account = ""
    container = "os-image"
    blob = ""
    blob_ext = ".vhd"
    windows_blob_url = "blob.core.windows.net"
    media_link = ""

    #SSH Keys
    azure_config = os.environ["HOME"] + '/.azure'
    thumbprint_path = azure_config + '/.ssh/thumbprint'
    public_key_path = azure_config + '/.ssh/myCert.pem'
    private_key_path = azure_config + '/.ssh/myPrivateKey.key'
    key_pair_path = private_key_path

    #Adding for cluster
    num_4_win = 0
    num_4_lin = 4
    cluster_count = num_4_win + num_4_lin

    def __init__(self):
        self.set_name()
        self.set_location()
        return

    def set_name(self, name=None):
        if not name:
            name = 'myvm-' + self.get_random()
        self.name = name

    def get_name(self):
        return self.name
        
    def get_random(self):
        return ''.join(str(x) for x in random.sample(range(0,10), 5))

    def set_location(self):
        '''This is temporary. the location should be defined in the azure.config
        file.'''
        self.location = "Central US"

    def get_config(self):
        self.get_creds()
        return

    def get_creds(self):
        self.cert = Credentials()

        self.subscription_id = self.cert.getSubscription()
        self.certificate_path = self.cert.getManagementCertFile()

    def create_vm(self, name=None, location=None):
        self.set_name(name)
        self.connect_service()
        self.create_cloud_service(name, location)
        self.get_image_name()
        self.get_media_link(blobname=name)

        os_hd = OSVirtualHardDisk(self.image_name, self.media_link)
        linux_user_id = 'azureuser'
        linux_user_passwd = 'mypassword1234@'
        linux_config = LinuxConfigurationSet(self.get_name(), linux_user_id, linux_user_passwd, False)

        self.set_ssh_keys(linux_config)
        self.set_network()
        self.set_service_certs()

        result = \
        self.sms.create_virtual_machine_deployment(service_name=self.get_name(), \
                                                   deployment_name=self.get_name(), \
                                                   deployment_slot='production',\
                                                   label=self.get_name(), \
                                                   role_name=self.get_name(), \
                                                   system_config=linux_config, \
                                                   os_virtual_hard_disk=os_hd, \
                                                   network_config=self.network,\
                                                   role_size='Small')

        self.result = result
        return result

    def connect_service(self, refresh=False):
        if not self.sms or refresh:
            self.sms = ServiceManagementService(self.subscription_id, self.certificate_path)

    def create_cloud_service(self, name=None, location=None):
        if not name:
            name = self.get_name()
        if not location:
            location = self.location
        self.sms.create_hosted_service(service_name=name, label=name, location=location)

    def set_ssh_keys(self, config):
        self.thumbprint = open(self.thumbprint_path, 'r').readline().split('\n')[0]
        publickey = PublicKey(self.thumbprint, self.public_key_path)
        keypair = KeyPair(self.thumbprint, self.key_pair_path)
        config.ssh.public_keys.public_keys.append(publickey)
        config.ssh.key_pairs.key_pairs.append(keypair)

    def set_network(self):
        network = ConfigurationSet()
        network.configuration_set_type = 'NetworkConfiguration'
        network.input_endpoints.input_endpoints.append(ConfigurationSetInputEndpoint('ssh', 'tcp', '22', '22'))
        self.network = network

    def set_service_certs(self):
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
        return self.sms.list_os_images()

    def list_storage_accounts(self):
        return self.sms.list_storage_accounts()

    def get_status(self, request_id=None):
        if not request_id:
            request_id = self.result.request_id
        return self.sms.get_operation_status(request_id)

    def get_deployment(self):
        return self.sms.get_deployment_by_name(service_name=self.get_name(),
                                               deployment_name=self.get_name())

    def get_image_name(self):
        '''Return OS Image name'''
        '''temporarily fixed image is set'''
        result = self.sms.list_os_images()
        #Let's find images and pick the last one which might be the latest.
        for image in result:
            if image.os == "Linux":
                if image.category == "Canonical":
                    try:
                        if image.label.index("12.04"):
                            image_name = image.name
                            os_name = image.os
                    except:
                        pass
        self.image_name = image_name
        self.os_name = os_name

    def get_media_link(self, storage_account=None, container=None, blobname=None):
        '''Return a media link'''
        if not storage_account:
            storage_account = self.get_storage_account()
        if not blobname:
            blobname = self.get_name()
        blob_prefix = self.os_name
        blob = blob_prefix + "-" + blobname + self.blob_ext
        media_link = "http://" + storage_account + "." + self.windows_blob_url \
                + "/" + self.container + "/" + blob
        self.media_link = media_link
        return media_link

    def get_storage_account(self, refresh=False):
        '''Return the last storage account name'''
        if not self.storage_account or refresh:
            result = self.sms.list_storage_accounts()
            for account in result:
                storage_account = account.service_name
            self.storage_account = storage_account
        return self.storage_account

    def create_cluster(self, num=None, option=None):
        '''Create multiple VMs to support cluster computing'''

        if not num:
            cluster_count = self.cluster_count
        results = []
        # It is supposed to use multi-processing instead of for loop
        for cnt in range(cluster_count):
            self.set_name("my-cluster-vm-" + str(cnt) + "-" + self.get_random())
            result = self.create_vm(self.get_name())
            sleep(10)
            results.append(result)

            #media_link = self.get_media_link(blobname=new_name)
            #self.create_cloud_service(name=new_name)
            #temporarily added waiting time for deploying cloud service

