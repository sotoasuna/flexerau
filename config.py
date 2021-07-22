'''
Created on Sep 14, 2019

@author: SGeary
'''

FNCI_HOST = "localhost"
FNCI_PORT = "8888"
BASEURL = "http://" + FNCI_HOST + ":" + FNCI_PORT + "/codeinsight/api/"
# Token for Workflow Admin User  ( must be added to project to update task)
ADMIN_AUTHTOKEN = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJhZG1pbiIsInVzZXJJZCI6MSwiaWF0IjoxNTgwMjE2MDg0fQ.rHPyLbJ24BZbmN3ng0WLJH2pKsQgv2aklaGs3jAJMYxKHKBm_Qp8J_WXL93s_sQIh_zynEKjGGIim_giKgXajQ"
AUTHTOKEN = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJvb3duZXIiLCJ1c2VySWQiOjYsImlhdCI6MTU4MDI5OTQzN30.LuxiDTgRSked1guyADNK3CMZIIDaUHDXwyTPLc_77rvhDW6d4GVUfK6SNXRntHZGpGScnzPoq9UeOzdjUbXyCQ"

v6_FNCI_HOST = "localhost"
v6_FNCI_PORT = "8880"
v6_BASEURL = "http://" + v6_FNCI_HOST + ":" + v6_FNCI_PORT + "/palamida/api/"
v6_REQUESTURL = "http://" + v6_FNCI_HOST + ":" + v6_FNCI_PORT + "/palamida/RequestDetails.htm?rid="

# Token for Workflow Admin User
# This user must own the template project!
v6_AUTHTOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ3b3JrZmxvd2FkbWluIiwiaWF0IjoxNTc2NzYwNzAzfQ.3eIPBdUwapkw0kVyW1AatEkvlZt1ygiidGbIxFmSfTk"
v6_teamName = "Engineering"
v6_projectTemplatename = "Workflow Template"  # Must be owned by user with Auth Token above

# To allow for changes in script that are release specific
FNCI_VERSION = "2020R1"