import os
import sys

from azure import *
from azure.servicemanagement import *

class TheCloud:
    def __init__(self):
        self.subscription_id = None
        self.certificate_path = None
        self.sms = None

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

    def _get_service(self):
        if not self.sms:
            self.sms = ServiceManagementService(self.subscription_id, self.certificate_path)
        return self.sms
 
    def create_vm(self):
       
        name = 'thecloudtest1'
        location = 'Central US'
        sms = self._get_service()

        # You can either set the location or an affinity_group
        sms.create_hosted_service(service_name=name, label=name, location=location)

        # Name of an os image as returned by list_os_images
        image_name = 'ipnb'

        # Destination storage account container/blob where the VM disk
        # will be created
        media_link = \
        "http://portalvhdsdhxy08ht1l8wq.blob.core.windows.net/vhds/fmr1wqtr.fww201305292239460030.vhd"

        # Linux VM configuration, you can use WindowsConfigurationSet
        # for a Windows VM instead
        linux_config = LinuxConfigurationSet('myhostname12q3', 'azureuser',
                                             '1234qwer`', True)

        os_hd = OSVirtualHardDisk(image_name, media_link)

        sms.create_virtual_machine_deployment(service_name=name,
                deployment_name=name,
                deployment_slot='production',
                label=name,
                role_name=name,
                system_config=linux_config,
                os_virtual_hard_disk=os_hd,
                role_size='Small')

    def test_list_location(self):
        sms = self._get_service()

        result = sms.list_locations()
        for location in result:
            print(location.name)

    def test_list_os_images(self):
        sms = self._get_service()
        result = sms.list_os_images()

        for image in result:
            print('Name: ' + image.name)
            print('Label: ' + image.label)
            print('OS: ' + image.os)
            print('Category: ' + image.category)
            print('Description: ' + image.description)
            print('Location: ' + image.location)
            print('Affinity group: ' +
                  image.affinity_group)
            print('Media link: ' +
                  image.media_link)
            print('')

if __name__ == "__main__":
    c = TheCloud()
    c.load_certificate()
    # create vm didnt work...
    c.create_vm()
    #c.test()
    #c.test_list_os_images()
