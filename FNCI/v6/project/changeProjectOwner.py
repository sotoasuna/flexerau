'''
Created on Nov 19, 2019

@author: SGeary
'''
import logging
import requests

import config

ENDPOINT_URL = config.v6_BASEURL + "project/changeProjectOwner/"

logger = logging.getLogger(__name__)

#-----------------------------------------------------------------------#
def change_project_owner(projectID, ownerID, authToken):
    logger.debug("Entering change_project_owner")
   
    changeProjectOwnerBody = get_changeProjectOwnerBody(projectID, ownerID) 
    logger.debug("changeProjectOwnerBody:  %s"  %changeProjectOwnerBody)
             
    headers = {'Content-Type': 'application/json', 'Authorization': authToken}  
    RESTAPI_URL = ENDPOINT_URL
    logger.debug("    RESTAPI_URL: %s" %RESTAPI_URL)
    logger.debug("        headers: %s" %headers)  
       
    try:
        response = requests.post(RESTAPI_URL, data=changeProjectOwnerBody, headers=headers)
        
    except requests.exceptions.RequestException as e:
        print(e)
        logger.debug(e)
        logger.debug(response)
        logger.debug(response.text)
        return False
    
    # Check the response code and proceed accordingly
    if response.status_code == 200:
        logger.debug("Project owner changed")


    elif response.status_code == 401:
        print("Unauthorized - change_project_owner")
        logger.debug("Unauthorized - change_project_owner")            
    
    elif response.status_code == 404:
        print("Bad Request")
    
    elif response.status_code == 500:
        print("Internal Server Error")
#-----------------------------------------------------------#

 
def get_changeProjectOwnerBody(projectID, ownerID) : 

      
    changeProjectOwnerBody = '''    {
    "projectId" :"''' + str(projectID) +  '''",
    "userId" :"''' + str(ownerID) + '''"
}'''
     
    return changeProjectOwnerBody            
            