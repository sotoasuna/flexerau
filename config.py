'''
Created on Sep 14, 2019

@author: SGeary
'''

FNCI_HOST = "localhost"
BASEURL = "http://" + FNCI_HOST + ":8888/codeinsight/api/"
AUTHTOKEN = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJkZGV2ZWxvcGVyIiwidXNlcklkIjoyLCJpYXQiOjE1Njg0OTI4NTN9.tHOZdQrSXcQo3xC8RpJEEFAn-tG2sPTdu85qZSi4iqgve_uD4U2xXc69NX2-0ob2z6xaRhUSRikVqY6YE51v7A"

v6_FNCI_HOST = "smg.flexnetcodeinsight.com"
v6_BASEURL = "http://" + v6_FNCI_HOST + ":8888/palamida/api/"
v6_AUTHTOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJkZGV2ZWxvcGVyIiwiaWF0IjoxNTY4NDY4ODUyfQ.MhrYUJTkHCDpTmIGPMK-a1moGuxOUDFZz--uL870dzM"
v6_teamName = "Engineering"

#--------------------------------------------------------------------------#
#  Dictionary to contain the inventory ID to Workflow Request mappings
#  until the synchronize ID is added to the inventory JSON response
#
INVENTORYITEM_REQUESTS = {}
# INVENTORYITEM_REQUESTS["inventory item in v7"]  = "request ID in v6"
INVENTORYITEM_REQUESTS[1]=4  #  jquery.jquery
INVENTORYITEM_REQUESTS[2]=5  #  jlibpng

'''

    "request": [
        {
            "v7_inventoryId": 1,
            "v6_request": 4,
            "componentName": "jquery.jquery"
        }
        {
            "v7_inventoryId": 2,
            "v6_request": 4,
            "componentName": "jlibpng"
        }
    ]


'''
