'''
Created on Aug 15, 2019

@author: SGeary
'''

import logging
import requests
import json

import config


logger = logging.getLogger(__name__)

INVENTORY_ENDPOINT_URL = config.BASEURL + "project/inventory/"

#--------------------------------------------------------------------#
def get_project_inventory(projectID, authToken):
    logger.info("Entering get_project_inventory")
    
    RESTAPI_URL = INVENTORY_ENDPOINT_URL + str(projectID) + "?published=true&size=100&page=1" 
    
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + authToken} 
       
    logger.debug("    RESTAPI_URL: %s" %RESTAPI_URL)

    # Make the REST API call with the project data           
    response = requests.get(RESTAPI_URL, headers=headers)
    logger.debug(json.dumps(response.json(), indent=3))

       
    #------------------------------------------------------------------------------------#   
    # Now parse the results from the REST call
    if "inventoryItems" in response.json(): 
        # The project ID was returned
        INVENTORY = (response.json()["inventoryItems"])
        # In this case we are strictly returning the inventory only
        return INVENTORY

    elif "Error: " in response.json():
        errorKey = response.json()["Key: "]
        errorMessage = response.json()["Error: "]
        
        print("Error in getting project ID")
        print("   %s:  %s" %(errorKey, errorMessage))
        print("")
        return(False)
        
    else:
        logger.error("Unknown data in response")
        return  


#--------------------------------------------------------------------------#

def get_project_name_by_id(projectID, authToken):
    logger.info("Entering get_project_name_by_id")
    
    RESTAPI_URL = INVENTORY_ENDPOINT_URL + str(projectID) + "?published=true&size=100&page=1" 
    
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + authToken} 
       
    logger.debug("    RESTAPI_URL: %s" %RESTAPI_URL)

    # Make the REST API call with the project data           
    response = requests.get(RESTAPI_URL, headers=headers)
    logger.debug(json.dumps(response.json(), indent=3))
       
    #------------------------------------------------------------------------------------#   
    # Now parse the results from the REST call
    if "projectName" in response.json(): 
        # The project ID was returned
        projectName = (response.json()["projectName"])
        # In this case we are strictly returning the inventory only

        return projectName

    elif "Error: " in response.json():
        errorKey = response.json()["Key: "]
        errorMessage = response.json()["Error: "]
        
        logger.debug("Error in getting project ID")
        logger.debug("   %s:  %s" %(errorKey, errorMessage))

        return("False")  # Not sure why I could not return False as boolean
        
    else:
        logger.error("Unknown data in response")
        return("False")  


#----------------------------------------------------------------------------#
def get_project_owner_email_id(projectID, authToken):
    logger.info("Entering get_project_owner_email_id")
    
    RESTAPI_URL = INVENTORY_ENDPOINT_URL + str(projectID) + "?published=true&size=100&page=1" 
    
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + authToken} 
       
    logger.debug("    RESTAPI_URL: %s" %RESTAPI_URL)

    # Make the REST API call with the project data           
    response = requests.get(RESTAPI_URL, headers=headers)
    logger.debug(json.dumps(response.json(), indent=3))
       
    #------------------------------------------------------------------------------------#   
    # Now parse the results from the REST call
    if "ownerEmail" in response.json(): 
        # The project ID was returned
        ownerEmail = (response.json()["ownerEmail"])
        # In this case we are strictly returning the inventory only

        return ownerEmail

    elif "Error: " in response.json():
        errorKey = response.json()["Key: "]
        errorMessage = response.json()["Error: "]
        
        print("Error in getting project ID")
        print("   %s:  %s" %(errorKey, errorMessage))
        print("")
        return(False)
        
    else:
        logger.error("Unknown data in response")
        return      
