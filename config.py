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
v6_projectTemplatename = "WF_Template"

#--------------------------------------------------------------------------#
#  External file to hold the project/inventory/task/request mappings
#  This will be replaced when the request ID is returned as part of the
#  get invetory requset API call in v7
#
RTI_MAPPINGS_DIRECTORY = "RTI_DATAFILES/"
RTI_MAPPINGS_FILE_SUFFIX = "requests_mappings.json"

#----------------------------------------------------------------------------#
#  MySQL DAtabase details to hold the place for a new API in v7 (2019R4??) for user data

mySQLHOST = "localhost"
mySQLUSER = "fnciuser"
mySQLPASSWORD = "Fnci%1234"
mySQLDATABASE = "2019r3_82"

