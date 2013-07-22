import os
import base64
from azure import *
from azure.servicemanagement import *
from ext.credentials import Credentials

class SimpleAzure:

        config_path = os.environ["HOME"] + "/.azure/"
        subscription_id = ""
        certificate_path = ""

        name = ""
        location = ""

        image_name = ""

        # Storage
        storage_account = ""
        container = ""
        blob = ""
        windows_blob_url = "blob.core.windows.net"
        media_link = "http://" + storage_account + "." + windows_blob_url + "/" + container + "/" + blob

        #SSH Keys
        azure_config = os.environ["HOME"] + '/.azure'
        thumbprint_path = azure_config + '/.ssh/thumbprint'
        public_key_path = azure_config + '/.ssh/myCert.pem'
        private_key_path = azure_config + '/.ssh/myPrivateKey.key'
        key_pair_path = private_key_path
        thumbprint=open(thumbprint_path, 'r').readline().split('\n')[0]

        def __init__(self):
                return

        def get_config(self):
                self.get_creds()
                return

        def get_creds(self):
                self.cert = Credentials()

                self.subscription_id = self.cert.getSubscription()
                self.certificate_path = self.cert.getManagementCertFile()

        def create_vm(self):
                self.load_service()
                self.create_cloud_service()

                os_hd = OSVirtualHardDisk(self.image_name, self.media_link)
                linux_user_id = 'azureuser'
                linux_user_passwd = 'mypassword1234@'
                linux_config = LinuxConfigurationSet(self.name, linux_user_id, linux_user_passwd, False)

                self.set_ssh_keys(linux_config)
                self.set_network()
                self.set_service_certs()

                result = self.sms.create_virtual_machine_deployment(service_name=self.name,
                                deployment_name=self.name,
                                deployment_slot='production',
                                label=self.name,
                                role_name=self.name,
                                system_config=linux_config,
                                os_virtual_hard_disk=os_hd,
                                network_config=self.network,
                                role_size='Small')

                self.result = result
                return result

        def load_service(self):
                self.sms = ServiceManagementService(self.subscription_id, self.certificate_path)

        def create_cloud_service(self, name=None, location=None):
                if not name:
                        name = self.name
                if not location:
                        location = self.location
                self.sms.create_hosted_service(service_name=name, label=name, location=location)

        def set_ssh_keys(self, config):
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
                cert_res = self.sms.add_service_certificate(service_name=self.name,
                                data=cert_data,
                                certificate_format=cert_format,
                                password=cert_password)

                self.cert_return = cert_res

        def list_images(self):
                return self.sms.list_os_images()

        def list_storage_accounts(self):
                return self.sms.list_storage_accounts()

        def get_status(self):
                return self.sms.get_operation_status(request_id)

        def get_deployment(self):
                return self.sms.get_deployment_by_name(service_name=self.name, deployment_name=self.name)
