'''
Created on Nov 13, 2019

@author: SGeary
'''
import logging
import requests
import json

import config


logger = logging.getLogger(__name__)

ENDPOINT_URL = config.BASEURL + "inventories"

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
    RESTAPI_URL = ENDPOINT_URL +  "/" + str(inventoryID)
    logger.debug("    RESTAPI_URL: %s" %RESTAPI_URL)  
       
    try:
        response = requests.put(RESTAPI_URL, data=updateBody, headers=headers)
        logger.debug(json.dumps(response.json(), indent=3))  
        
    except requests.exceptions.RequestException as e:
        print(e)
        logger.debug(e)
        logger.debug(response)
        logger.debug(response.text)
        return False
    
        
    # Check the response code and proceed accordingly
    if response.status_code == 200:
        logger.debug("Update succeeded")

    elif response.status_code == 401:
        print("Unauthorized")        
    
    elif response.status_code == 404:
        print("Inventory with id of %s was not found" %inventoryID)
    
    elif response.status_code == 500:
        print("Internal Server Error")
        
        
#--------------------------------------------------#        
def get_updateBody(key, value): 

      
    updateBody = '''    {

     "''' + key + '''": "''' + value + '''"
    }'''
     
    return updateBody  
