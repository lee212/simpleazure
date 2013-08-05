# -*- coding: utf-8 -*-

"""
vmdepot.Community
~~~~~~~~~~~~~~~~~~~~~~~~

This module provides a Python library for Windows Azure Virtual Machines.

 :copyright: TBD
 :license: TBD

"""
import urllib2
import xml.etree.ElementTree as ET

class Community:
    """Supports to utilize community images

    Based on
    https://github.com/WindowsAzure/azure-sdk-tools-xplat/blob/master/lib/util/communityUtil.js
    
    """

    service_host = 'vmdepot.msopentech.com'
    service_url = '/OData.svc'

    def get_blob_url(self, uid):
        """Return BlobUrl for a uid

        e.g. uid = 'vmdepot-2440-1-1'
        returns
        http://vmdepotwestus.blob.core.windows.net/linux-community-store/community-2464-3ff1336d-e5d8-4485-9d37-fe0634ec18a7-1.vhd

        try 'http://vmdepot.msopentech.com/OData.svc/ResolveUid?uid='vmdepot-2440-1-1'
        on web browser

        """
        url = self.get_resolve_url(uid)
        data = self.get_xml_from_web(url)
        # Need to parse the strings like this
        '''
        <ResolveUid xmlns="http://schemas.microsoft.com/ado/2007/08/dataservices">
        <element
        xmlns:p2="http://schemas.microsoft.com/ado/2007/08/dataservices/metadata"
        p2:type="Bamako_ServiceModel.DeployVM">
        <BlobUrl>
        http://vmdepotwestus.blob.core.windows.net/linux-community-store/community-2464-3ff1336d-e5d8-4485-9d37-fe0634ec18a7-1.vhd
        </BlobUrl>
        <Location>West US</Location>
        </element>
        </ResolveUid>
        '''
        for blob in data.findall('ResolveUid'):
            print blob.find('BlobUrl').text

    def get_resolve_url(self, uid):
        resolve_url = "/ResolveUid"
        res = "http://" + self.service_host + self.service_url + resolve_url + \
        "?uid='" + uid + "'"
        return res

    def get_xml_from_web(self, url):
        """Return parsed xml from the url

        :returns: dict.

        """

        toursurl = urllib2.urlopen(url)
        toursurl_string = toursurl.read()
        #return parser.parseString( toursurl_string )
        root = ET.fromstring(toursurl_string)
        return root

if __name__ == "__main__":
    comm = Community()
    blob = comm.get_blob_url('vmdepot-2440-1-1')
    print blob
