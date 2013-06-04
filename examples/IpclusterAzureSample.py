import os
import sys

from azure import *
from azure.servicemanagement import *

class IpclusterAzureSample:
    def __init__(self):
        self.subscription_id = None
        self.certificate_path = None

    def load_certificate(self):
        try:
            self.subscription_id = os.environ.get('azure_subscription_id')
            self.certificate_path = os.environ.get('azure_certificate_path')
        except:
            print sys.exc_info()

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
    ipya = IpclusterAzureSample()
    ipya.load_certificate()
    ipya.create_vm()
