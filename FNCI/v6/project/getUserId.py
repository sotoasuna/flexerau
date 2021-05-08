'''
Created on Sep 19, 2019

@author: SGeary
'''
import logging
import requests
import json

import config


ID_ENDPOINT_URL = config.v6_BASEURL + "project/userId/"


logger = logging.getLogger(__name__)

#-----------------------------------------------------------------------#
def get_user_id_from_email(emailAddress, authToken):
    logger.debug("Entering get_project_id with email %s" %(emailAddress))
      
    headers = {'Content-Type': 'application/json', 'Authorization': authToken}  
    RESTAPI_URL = ID_ENDPOINT_URL + emailAddress 
    logger.debug("    RESTAPI_URL: %s" %RESTAPI_URL)  
    response = requests.get(RESTAPI_URL, headers=headers)
             
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
            
            if "Content" in response.json(): 
            
                userId = (response.json()["Content"])
                logger.debug("     User ID for %s is %s" %(emailAddress, userId))
                return userId
            
            else:
                errorMessage = (response.json()["Errors(s) "])
                print(errorMessage)
                print("Exiting script")
                exit()
                
        
        elif HttpStatusCode == 400:
            
            print("Unknown Error.  Please see log for details.....")  
        
        else:
            # Unknown status code that needs to be investigated
            logger.error("Unknown HttpStatusCode: %s" %response.json()["Error: "])
            print("Unknown Error.  Please see log for details.....")   
            
    else: 
        errorMessage = (response.json()["Error(s) "])
        
        if errorMessage["User not found "] == "System did not recognize the user email!":
            print("    - User with email address %s not found in workflow system" %emailAddress)
            print("    - Exiting......")
            exit()
        else:
            print(errorMessage)
            print("Exiting......")
            exit()
                      
