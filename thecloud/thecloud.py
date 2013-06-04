import os
import sys

from azure import *
from azure.servicemanagement import *

class TheCloud:
    def __init__(self):
        self.subscription_id = None
        self.certificate_path = None

        self.azure_name = "azure"
        
        self.rcfile = os.environ['HOME'] + "/" + self.azure_name + "/azurerc"
        # proposed configuration type is yaml instead of rc. however rc is still
        # popular.
        self.yamlfile = os.environ["HOME"] + "/" + self.azure_name + "/azure.yaml"

    def load_certificate(self):
        try:
            self.subscription_id = self.get_certificate('azure_subscription_id')
            self.certificate_path = self.get_certificate('azure_certificate_path')
        except:
            print sys.exc_info()

    def get_certificate(self, name):
        return os.getenv(name, self._default_certificate(name))
    
    def _default_certificate(self, name=None):
        clist = self._readrc()
        if name:
            return clist[name]
        return clist
        
    def _readrc(self, filename=None):
        if not filename:
            filename = self.rcfile

        res = {}
        c = open(filename, 'r')
        clist = c.readlines()
        for x in clist:
            v = x.replace('export ','').split('=')
            res[v[0]] = self._strip_spaces(v[1])

        return res

    def _strip_spaces(self, name):
        return "".join(name.replace("'", "").split())

    def create_vm(self):
        subscription_id = self.subscription_id
        certificate_path = self.certificate_path
        sms = ServiceManagementService(subscription_id, certificate_path)
        name = 'myvm'
        location = 'West US'

        # You can either set the location or an affinity_group
        sms.create_hosted_service(service_name=name, label=name, location=location)

        # Name of an os image as returned by list_os_images
        image_name = 'OpenLogic__OpenLogic-CentOS-62-20120531-en-us-30GB.vhd'

        # Destination storage account container/blob where the VM disk
        # will be created
        media_link = 'url_to_target_storage_blob_for_vm_hd'

        # Linux VM configuration, you can use WindowsConfigurationSet
        # for a Windows VM instead
        linux_config = LinuxConfigurationSet('myhostname', 'myuser', 'mypassword', True)

        os_hd = OSVirtualHardDisk(image_name, media_link)

        sms.create_virtual_machine_deployment(service_name=name,
                deployment_name=name,
                deployment_slot='production',
                label=name,
                role_name=name,
                system_config=linux_config,
                os_virtual_hard_disk=os_hd,
                role_size='Small')

    def test(self):
        subscription_id = self.subscription_id
        certificate_path = self.certificate_path

        sms = ServiceManagementService(subscription_id, certificate_path)

        result = sms.list_locations()
        for location in result:
            print(location.name)

if __name__ == "__main__":
    c = TheCloud()
    c.load_certificate()
    c.test()
    # create vm didnt work...
    #ipya.create_vm()
