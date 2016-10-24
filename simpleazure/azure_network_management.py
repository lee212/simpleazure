# Test for getting ip address
from azure.mgmt.network import NetworkManagementClient as nmc

class AzureNetworkManagement(object):
    def __init__(self, credentials = None, subscription_id = None):
        if credentials and subscription_id:
            self.cred = credentials
            self.sid = subscription_id
        if self.cred and self.sid:
            self.client = nmc(self.cred, self.sid)

    def set_credentials(self, credentials, subscription_id):
        self.cred = credentials
        self.sid = subscription_id

    def set_resource_group(self, group_name):
        self.resource_group = group_name

    # public ip address in this example
    def get_access_info(self, resource_group=None):
        res = []
        try:
            ips = self.client.public_ip_addresses.list(resource_group or self.resource_group)
            # {'dns_settings': None, 'name': u'fp6mwq3k4ytsypublicip', 'tags': None, 'public_ip_address_version': u'IPv4', 'public_ip_allocation_method': u'Dynamic', 'resource_guid': u'24d9fc7a-8ff0-40da-9b88-e283e105c07c', 'provisioning_state': u'Succeeded', 'ip_address': u'40.83.13.177', 'etag': u'W/"1ea1dc32-6afc-4704-b927-d7f5db69d4da"', 'location': u'centralus', 'ip_configuration': <azure.mgmt.network.models.ip_configuration.IPConfiguration object at 0x7f56bd981890>, 'idle_timeout_in_minutes': 4, 'type': u'Microsoft.Network/publicIPAddresses', 'id': u'/subscriptions/6b3cf2b5-2cc1-4828-b5e0-9f8be72e6e6f/resourceGroups/saz-rg/providers/Microsoft.Network/publicIPAddresses/fp6mwq3k4ytsypublicip'}
            for ip in ips:
                res.append(ip.ip_address)
            return res
        except:
            return res
