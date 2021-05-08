'''
Created on Sep 16, 2019

@author: SGeary
'''

import logging
import requests
import json

import config


WORKFLOW_ENDPOINT_URL = config.v6_BASEURL + "workflow/createRequest/"


logger = logging.getLogger(__name__)

#-----------------------------------------------------------------------#
def create_workflow_request(REQUESTDETAILS, authToken):
    logger.debug("Entering create_workflow_request")
    logger.debug("REQUESTDETAILS: %s" %REQUESTDETAILS)
    
    
    createRequestBody = get_createRequestBody(REQUESTDETAILS) 
      
    headers = {'Content-Type': 'application/json', 'Authorization': authToken}  
    RESTAPI_URL = WORKFLOW_ENDPOINT_URL
    logger.debug("    RESTAPI_URL: %s" %RESTAPI_URL)  
    response = requests.post(RESTAPI_URL, data=createRequestBody, headers=headers)
             
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
                print(response.json()["Content"])
                exit()

        
        else:
            # Unknown status code that needs to be investigated
            logger.error("Unknown HttpStatusCode: %s" %response.json()["Error: "])
            print("Unknown Error.  Please see log for details.....")   
            exit()
 
    else:
        print("Unknown Error.  Please see log for details.....")   
        exit()
#-----------------------------------------------------------#
 
def get_createRequestBody(REQUESTDETAILS): 
    
    projectID = REQUESTDETAILS[0]
    requesterId = REQUESTDETAILS[1]
    ownerId = REQUESTDETAILS[2] 
    componentIdForTask = REQUESTDETAILS[3]
    componentVersionIdForTask = REQUESTDETAILS[4]
    selectedLicenseIdForTask = REQUESTDETAILS[5]
      
    createRequestBody = '''    {
    "versionId": ''' + str(componentVersionIdForTask) + ''',
    "reviewStatus": "draft",
    "projectId": ''' + str(projectID) + ''',
    "requesterId": ''' + str(requesterId) + ''',
    "ownerId": ''' + str(ownerId) + ''',
     "component": {
         "id": ''' + str(componentIdForTask) + '''
     },
     "fieldValues": {


     },
     "license": {
         "id": ''' + str(selectedLicenseIdForTask) + '''
     }
}'''
     
    return createRequestBody            
            