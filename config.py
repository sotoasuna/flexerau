'''
Created on Sep 14, 2019

@author: SGeary
'''

FNCI_HOST = "localhost"
FNCI_PORT = "8888"
BASEURL = "http://" + FNCI_HOST + ":" + FNCI_PORT + "/codeinsight/api/"
# Token for Workflow Admin User  ( must be added to project to update task)
ADMIN_AUTHTOKEN = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ3b3JrZmxvd19hZG1pbiIsInVzZXJJZCI6OCwiaWF0IjoxNTczNjQxNzAzfQ.gWzqpNgcsJ1X1PuAMd-y1jpLYaF17lfHXhVjVBdzJox4AkUZKsQwo7ngZBCxZ9M7W6wXc6sTZVXyfQqRmdyGvA"
AUTHTOKEN = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJvb3duZXIiLCJ1c2VySWQiOjUsImlhdCI6MTU3MzQ3OTE5MH0.qq874IWhQC44Ns5iU0xh_8p2R4CpdMVWuVSqD2qNDO5Kw74REzE4gu95xsohBx9Gc4IUdXlfrQ9FA7wGOXMkSg"

v6_FNCI_HOST = "localhost"
v6_FNCI_PORT = "8880"
v6_BASEURL = "http://" + v6_FNCI_HOST + ":" + v6_FNCI_PORT + "/palamida/api/"
v6_REQUESTURL = "http://" + v6_FNCI_HOST + ":" + v6_FNCI_PORT + "/palamida/RequestDetails.htm?rid="

# Token for Workflow Admin User
# This user must own the template project!
v6_AUTHTOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ3b3JrZmxvd2FkbWluIiwiaWF0IjoxNTc2NzYwNzAzfQ.3eIPBdUwapkw0kVyW1AatEkvlZt1ygiidGbIxFmSfTk"
v6_teamName = "Engineering"
v6_projectTemplatename = "Workflow Template"  # Must be owned by user with Auth Token above

