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


    workflowURLUpdateBody = get_workflowURLUpdateBody(requestURL) 
    logger.debug("workflowURLUpdateBody:  %s"  %workflowURLUpdateBody)
      
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + authToken}    
    RESTAPI_URL = ENDPOINT_URL +  "/" + str(inventoryID)
    logger.debug("    RESTAPI_URL: %s" %RESTAPI_URL)  
       
    try:
        response = requests.put(RESTAPI_URL, data=workflowURLUpdateBody, headers=headers)
        logger.debug(json.dumps(response.json(), indent=3))  
        
    except requests.exceptions.RequestException as e:
        print(e)
        logger.debug(e)
        logger.debug(response)
        logger.debug(response.text)
        return False
    
        
    # Check the response code and proceed accordingly
    if response.status_code == 200:
        logger.debug("workflowURL Updated with requestURL: %s" %requestURL)

    elif response.status_code == 401:
        print("Unauthorized")        
    
    elif response.status_code == 404:
        print("Inventory with id of %s was not found" %inventoryID)
    
    elif response.status_code == 500:
        print("Internal Server Error")
        
        
#--------------------------------------------------#        
def get_workflowURLUpdateBody(URL): 

      
    workflowURLUpdateBody = '''    {

     "workflowURL": "''' + URL + '''"
    }'''
     
    return workflowURLUpdateBody             