Import Account credentials
-------------------------------------------------------------------------------

It requires to use azure client tool to decode contents in xml files.

- In classic way of using azure is via servicemanagementcertificate, which can be downloaded from:
  http://go.microsoft.com/fwlink/?LinkId=254432
- ``*credentials.publishsettings`` xml file contains subscription id and encoded managementcertificate.
  ::

    <?xml version="1.0" encoding="utf-8"?>
	<PublishData>
	  <PublishProfile
	    SchemaVersion="2.0"
	    PublishMethod="AzureServiceManagementAPI">
	    <Subscription
	      ServiceManagementUrl="https://management.core.windows.net"
	      Id="6b3cf2b5-2cc1-4828-b5e0-9f8be72e6e6f"
	      Name="Pay-As-You-Go"
	      ManagementCertificate="MII...7nlV" />
	  </PublishProfile>
	</PublishData>

- ``azure account import <filename>`` reads and decodes the contents includeing ``ManagementCertificate`` and
stores a new file in JSON format under ``$HOME/.azure/azureProfile.json`` which looks like::

  {
    "environments": [],
    "subscriptions": [
        {
            "id": "6b*-2*-4*-b*-9*",
            "name": "Pay-As-You-Go",
            "user": {
                "name": "azure@gmail.com",
                "type": "user"
            },
            "managementCertificate": {
                "key": "-----BEGIN RSA PRIVATE KEY-----\n ... 4zhGrEBcX1P0=\n-----END RSA PRIVATE KEY-----\n",
                "cert": "-----BEGIN CERTIFICATE-----\n ... TtvBOUFM8kOVxZ/8xulQ==\n-----END CERTIFICATE-----\n"
            },
            "tenantId": "1ee-c1a-4de-8fe-2a51ef8fb",
            "state": "Enabled",
            "isDefault": true,
            "registeredProviders": [],
            "environmentName": "AzureCloud",
            "managementEndpointUrl": "https://management.core.windows.net"
        }
    ]
   }


- ``azure account cert export`` creates a managementCertificate.pem file which
  contains ``key`` and ``cert`` from ``"managementCertificate"``


Issue on decoding managementcertificate without azure cli tool
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

It supposes to decode:

- read XML from publishsettings file
  ::
   
	from xmljson import badgerfish as bf     
	from xml.etree.ElementTree import fromstring

	f = open("<filepath>","r");
	data = f.read()
	json_data = bf.data(fromstring(data))
	subscription = json_data['PublishData']['PublishProfile']['Subscription']
	sid = subscription['@Id']
	scert = subscription['@ManagementCertificate']
	f.close()

- decode with base64

  ::

	f2 = open("myCert.pfx","w")
	f2.write(scert.decode('base64'))
	f2.close()

- stuck with

   - https://github.com/Azure/azure-xplat-cli/blob/984313e0715f5b093955df532af5d48bf7828039/lib/util/profile/publishSettings.js#L41
   - https://github.com/Azure/azure-xplat-cli/blob/984313e0715f5b093955df532af5d48bf7828039/lib/util/certificates/pkcs.js#L85

