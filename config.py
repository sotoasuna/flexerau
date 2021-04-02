'''
Created on Sep 14, 2019

@author: SGeary
'''

FNCI_HOST = "localhost"
BASEURL = "http://" + FNCI_HOST + ":8888/codeinsight/api/"
AUTHTOKEN = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJkZGV2ZWxvcGVyIiwidXNlcklkIjo1LCJpYXQiOjE1Njg5NzM1Mzd9.NbI-dI6YPMJIjqpPph0cmzZK7phtSdwVJ0H-fY9q_HS35sZtcSx54wUJShXz5Nz8n7c5QIOrlUMrbpfbAS3IrA"

v6_FNCI_HOST = "smg.flexnetcodeinsight.com"
v6_BASEURL = "http://" + v6_FNCI_HOST + ":8888/palamida/api/"
v6_AUTHTOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJkZGV2ZWxvcGVyIiwiaWF0IjoxNTY4NDY4ODUyfQ.MhrYUJTkHCDpTmIGPMK-a1moGuxOUDFZz--uL870dzM"
v6_teamName = "Engineering"


#-------------------------------------------------#

v6_USERIDS = {}
v6_USERIDS["ddeveloper"] = 2 
#--------------------------------------------------------------------------#
#  Dictionary to contain the inventory ID to Workflow Request mappings
#  until the synchronize ID is added to the inventory JSON response
#
INVENTORYITEM_REQUESTS = {}
# INVENTORYITEM_REQUESTS["inventory item in v7"]  = "request ID in v6"
INVENTORYITEM_REQUESTS[3]=23  #  openwrt
INVENTORYITEM_REQUESTS[5]=24  #  libpng

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
