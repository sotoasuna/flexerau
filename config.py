'''
Copyright 2020 Flexera Software LLC
See LICENSE.TXT for full license text
SPDX-License-Identifier: MIT

Created on Sep 14, 2019

@author: SGeary
'''

FNCI_HOST = "localhost"
FNCI_PORT = "8888"
BASEURL = "http://" + FNCI_HOST + ":" + FNCI_PORT + "/codeinsight/api/"
# Token for Workflow Admin User  ( must be added to project to update task)
ADMIN_AUTHTOKEN = "v7 ADMIN JWT TOKEN"
AUTHTOKEN = "v7 USER JWT TOKEN"

v6_FNCI_HOST = "localhost"
v6_FNCI_PORT = "8880"
v6_BASEURL = "http://" + v6_FNCI_HOST + ":" + v6_FNCI_PORT + "/palamida/api/"
v6_REQUESTURL = "http://" + v6_FNCI_HOST + ":" + v6_FNCI_PORT + "/palamida/RequestDetails.htm?rid="

# Token for Workflow Admin User
# This user must own the template project!
v6_AUTHTOKEN = "v6ADMIN JWT TOKEN"
v6_teamName = "Engineering"  # The team that owns the template project to be copyied
v6_projectTemplatename = "Workflow Template"  # The project template be owned by user with Auth Token above

# To allow for changes in script that are release specific
FNCI_VERSION = "2020R2"