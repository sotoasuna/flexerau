'''
Created on Sep 16, 2019

@author: SGeary
'''

import logging
import requests
import json

import config


WORKFLOW_ENDPOINT_URL = config.v6_BASEURL + "synchronize/createRequest/"


logger = logging.getLogger(__name__)

#-----------------------------------------------------------------------#
def create_workflow_request(REQUESTDETAILS, authToken):
    logger.debug("Entering create_workflow_request")
    
    
    createRequestBody = get_createRequestBody(REQUESTDETAILS) 
      
    headers = {'Content-Type': 'application/json', 'Authorization': authToken}  
    RESTAPI_URL = WORKFLOW_ENDPOINT_URL
    logger.debug("    RESTAPI_URL: %s" %RESTAPI_URL)  
    response = requests.get(RESTAPI_URL, data=createRequestBody, headers=headers)
             
    try:
        logger.debug(json.dumps(response.json(), indent=3))  
    except ValueError:
        # no JSON returned
        logger.debug(response)
        logger.debug(response.text)
        return  "FAILURE"
    
    # Now parse the results from the REST call
    if "HttpStatusCode" in response.json():
        HttpStatusCode = (response.json()["HttpStatusCode"]) 
        
        if  HttpStatusCode == 200:
            
            requestId = (response.json()["Content"]["id"])
            logger.debug("     Request ID for this request is %s" %(requestId))
            return requestId
        
        elif HttpStatusCode == 400:
            
                logger.info(response.json()["Message"])

        
        else:
            # Unknown status code that needs to be investigated
            logger.error("Unknown HttpStatusCode: %s" %response.json()["Error: "])
            print("Unknown Error.  Please see log for details.....")   
 

#-----------------------------------------------------------#
 
def get_createRequestBody(REQUESTDETAILS): 
    
    projectID = REQUESTDETAILS[0]
    projectName = REQUESTDETAILS[0]
    requesterId = REQUESTDETAILS[0]
    ownerId = REQUESTDETAILS[0] 
    componentIdForTask = REQUESTDETAILS[0]
    componentVersionIdForTask = REQUESTDETAILS[0]
    selectedLicenseIdForTask = REQUESTDETAILS[0]

    createRequestBody = '''{
    
        "versionId": ''' + componentVersionIdForTask + ''',
        "reviewStatus": "draft",
        "projectId": ''' + projectID + ''',
        "requesterId": ''' + requesterId + ''',
        "ownerId": ''' + ownerId + ''',
         "component": {
             "id": ''' + componentIdForTask + '''
         },
         "fieldValues": {

         },
         "license": {
             "id": ''' + selectedLicenseIdForTask + '''
         }
    
     
        } '''
        
    return createRequestBody            
            