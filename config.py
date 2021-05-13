'''
Created on Sep 14, 2019

@author: SGeary
'''

FNCI_HOST = "localhost"
BASEURL = "http://" + FNCI_HOST + ":8888/codeinsight/api/"
AUTHTOKEN = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJvb3duZXIiLCJ1c2VySWQiOjMsImlhdCI6MTU3MTc1MzU3MX0.mAXDEDFeqA01fzffqR3gRdYzMlZDDXnWRbC5Ipsp3i4MfV9T2cx_L_5ko6KWGdMgqM7iw_dDq6FBToqhcvHcGw"

v6_FNCI_HOST = "workflow.flexnetcodeinsight.com"
v6_BASEURL = "http://" + v6_FNCI_HOST + ":8888/palamida/api/"
v6_AUTHTOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJvb3duZXIiLCJpYXQiOjE1NzE3NTMzMDB9.l6T-2ChetV2ntWb8M261RM7CxovTSyahG7zkfJvar9Y"
v6_teamName = "Engineering"
v6_projectTemplatename = "WF_Template"

#--------------------------------------------------------------------------#
#  External file to hold the project/inventory/task/request mappings
#  This will be replaced when the request ID is returned as part of the
#  get inventory request API call in v7
#
RTI_MAPPINGS_DIRECTORY = "RTI_DATAFILES/"
RTI_MAPPINGS_FILE_SUFFIX = "requests_mappings.json"

#----------------------------------------------------------------------------#
#  MySQL DAtabase details to hold the place for a new API in v7 (2019R4??) for user data

mySQLHOST = "localhost"
mySQLUSER = "fnciuser"
mySQLPASSWORD = "Fnci%1234"
mySQLDATABASE = "2019R3"

