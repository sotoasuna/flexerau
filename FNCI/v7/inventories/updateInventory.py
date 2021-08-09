'''
Created on Nov 13, 2019

@author: SGeary
'''
import logging
import requests
import sys
from flask import abort
import config

logger = logging.getLogger(__name__)

#######################################################################
# If the calling app is a flask app then we can use
# the flask abort function to catch exceptions
# so see if its defined in a common config file
try: 
    FLASKAPP = config.FLASKAPP
except:
    FLASKAPP = False
#######################################################################

FNCI_API = "FNCI Update Inventory API"
ENDPOINT_URL = config.BASEURL + "inventories/"


#--------------------------------------------------------------------#
def update_inventory_item_workflowURL(inventoryID, requestURL, authToken):
    logger.debug("Entering update_inventory_item_workflowURL with inventoryID %s" %inventoryID)

    workflowUpdateBody = get_updateBody("workflowURL", requestURL) 
    logger.debug("workflowURLUpdateBody:  %s"  %workflowUpdateBody)
    
    update_inventory_item(inventoryID, workflowUpdateBody, authToken)
    
#--------------------------------------------------------------------#
def update_inventory_item_UsageGuidance(inventoryID, guidanceText, authToken):
    logger.debug("Entering update_inventory_item_UsageGuidance with inventoryID %s" %inventoryID)

    usageGuidanceUpdateBody = get_updateBody("usageGuidance", guidanceText) 
    logger.debug("usageGuidanceUpdateBody:  %s"  %usageGuidanceUpdateBody)
    
    update_inventory_item(inventoryID, usageGuidanceUpdateBody, authToken)  
    
#--------------------------------------------------------------------#    
def update_inventory_item(inventoryID, updateBody, authToken):
    logger.debug("Entering update_inventory_item with inventoryID %s" %inventoryID)

    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + authToken}    
    RESTAPI_URL = ENDPOINT_URL + str(inventoryID)
    logger.debug("    RESTAPI_URL: %s" %RESTAPI_URL)  
               
    #  Make the request to get the required data   
    try:
        response = requests.put(RESTAPI_URL, data=updateBody, headers=headers)
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        # Connection Error - Is the server up and running?
        abort_message = FNCI_API + " - Error Connecting to FNCI Server - " +  (ENDPOINT_URL).split("codeinsight")[0] # Get rid of everything after codeinsight in url
        logger.error("    %s" %(abort_message))

        if FLASKAPP:         
            # Using error code 500 (Internal Server Error) to cover connection errors
            # in the flask apps
            abort(500, FNCI_API + " - %s" %abort_message) 
        else:
            print(abort_message)
            print("Is the FNCI server running?")
            print("Exiting script")
            sys.exit() 
    except requests.exceptions.RequestException as e: # Catch the exception for the logs but process below
        logger.error(e)
    
        
    # We at least received a response from FNCI so check the status to see
    # what happened if there was an error or the expected data
    if response.status_code == 200:
        logger.debug("    Call to %s was successful." %FNCI_API)
    
    elif response.status_code == 400:
        # Bad Request
        logger.error("    %s - Error: %s -  Bad Request." %(FNCI_API, response.status_code ))
        if FLASKAPP:         
            abort(400, FNCI_API + " - Bad Request - Look at debug log for more details") 
        else:
            print("%s - Error: %s -  Bad Request." %(FNCI_API, response.status_code ))
            print("    Exiting script")
            sys.exit()   

    elif response.status_code == 401:
        # Unauthorized Access
        logger.error("    %s - Error: %s -  Authentication Failed: JWT token is not valid or user does not have correct permissions." %(FNCI_API, response.status_code ))
        if FLASKAPP:         
            abort(401, FNCI_API + " - Authentication Failed: JWT token is not valid or user does not have correct permissions.")
        else:
            print("%s - Error: %s -  Authentication Failed: JWT token is not valid or user does not have correct permissions." %(FNCI_API, response.status_code ))
            print("    Exiting script")
            sys.exit()   

    elif response.status_code == 404:
        # Not Found
        logger.error("    %s - Error: %s -  URL endpoint not found:  %s" %(FNCI_API, response.status_code,  RESTAPI_URL ))
        if FLASKAPP:         
            abort(400, FNCI_API + " - Bad Request - URL endpoint not found") 
        else:
            print("    %s - Error: %s -  URL endpoint not found:  %s" %(FNCI_API, response.status_code,  RESTAPI_URL ))
            print("    Exiting script")
            sys.exit()   

    elif response.status_code == 405:
        # Method Not Allowed
        logger.error("    %s - Error: %s -  Method (GET/POST/PUT//DELETE/ETC) Not Allowed." %(FNCI_API, response.status_code ))
        if FLASKAPP:         
            abort(405, FNCI_API + " - Method Not Allowed.")
        else:
            print("    %s - Error: %s -  Method (GET/POST/PUT//DELETE/ETC) Not Allowed." %(FNCI_API, response.status_code ))
            print("    Exiting script")
            sys.exit()  
        
    elif response.status_code == 500:
        # Internal Server Error
        logger.error("    %s - Error: %s -  Internal Server Error." %(FNCI_API, response.status_code ))
        if FLASKAPP:         
            abort(500, FNCI_API + " - Internal Server Error.")
        else:
            print("    %s - Error: %s -  Internal Server Error." %(FNCI_API, response.status_code ))
            print("    Exiting script")
            sys.exit()  
        
        
        
#--------------------------------------------------#        
def get_updateBody(key, value): 

      
    updateBody = '''    {

     "''' + key + '''": "''' + value + '''"
    }'''
     
    return updateBody  
