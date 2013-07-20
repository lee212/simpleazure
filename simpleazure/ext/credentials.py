# Copied from WindowsAzure/azure-sdk-for-python
# https://github.com/WindowsAzure/azure-sdk-for-python/blob/master/test/azuretest/util.py

import os
import json

class Credentials(object):
    '''
    Azure credentials needed to run Azure.
    '''
    def __init__(self):
        configFilename = os.environ["HOME"] + "/.azure/config.json"
        tmpName = os.path.join(os.getcwd(), configFilename)

        if not os.path.exists(tmpName):
            errMsg = "Cannot run Azure when the expected config file containing Azure credentials, '%s', does not exist!" % (tmpName)
            raise EnvironmentError(errMsg)

        with open(tmpName, "r") as f:
            self.ns = json.load(f)
        self.config_path = os.path.dirname(tmpName)

    def getManagementCertFile(self):
        try:
            return self.ns[u'managementcertfile']
        except:
            return self.config_path + "/managementCertificate.pem"
    def getSubscriptionId(self):
        return self.ns[u'subscriptionid']

    def getSubscription(self):
        return self.ns[u'subscription']

    def getServiceBusKey(self):
        return self.ns[u'servicebuskey']

    def getServiceBusNamespace(self):
        return self.ns[u'servicebusns']

    def getStorageServicesKey(self):
        return self.ns[u'storageserviceskey']

    def getStorageServicesName(self):
        return self.ns[u'storageservicesname']

    def getLinuxOSVHD(self):
        return self.ns[u'linuxosvhd']
