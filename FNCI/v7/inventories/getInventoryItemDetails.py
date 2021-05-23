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
def get_inventory_item_workflowURL_by_id(inventoryID, authToken):
    logger.debug("Entering get_inventory_item_workflowURL_by_id with inventoryID %s" %inventoryID)

    
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + authToken}  
    RESTAPI_URL = ENDPOINT_URL +  "/" + str(inventoryID)
    logger.debug("    RESTAPI_URL: %s" %RESTAPI_URL)  
       
    try:
        response = requests.get(RESTAPI_URL, headers=headers)
        logger.debug(json.dumps(response.json(), indent=3))  
        
    except requests.exceptions.RequestException as e:
        print(e)
        logger.debug(e)
        logger.debug(response)
        logger.debug(response.text)
        return False
    
    # Check the response code and proceed accordingly
    if response.status_code == 200:
        logger.debug(response.json()["data"]["workflowURL"])
        return(response.json()["data"]["workflowURL"])


    elif response.status_code == 401:
        print("Unauthorized")        
    
    elif response.status_code == 404:
        print("Inventory with id of %s was not found" %inventoryID)
    
    elif response.status_code == 500:
        print("Internal Server Error")
        
#--------------------------------------------------------------------#
def get_inventory_item_information_by_id(inventoryID, authToken):
    logger.debug("Entering get_inventory_item_information_by_id with inventoryID %s" %inventoryID)

    
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + authToken}  
    RESTAPI_URL = ENDPOINT_URL +  "/" + str(inventoryID)
    logger.debug("    RESTAPI_URL: %s" %RESTAPI_URL)  
       
    try:
        response = requests.get(RESTAPI_URL, headers=headers)
        logger.debug(json.dumps(response.json(), indent=3))  
        
    except requests.exceptions.RequestException as e:
        print(e)
        logger.debug(e)
        logger.debug(response)
        logger.debug(response.text)
        return False
    
    # Check the response code and proceed accordingly
    if response.status_code == 200:
        return(response.json()["data"])


    elif response.status_code == 401:
        print("Unauthorized")        
    
    elif response.status_code == 404:
        print("Inventory with id of %s was not found" %inventoryID)
    
    elif response.status_code == 500:
        print("Internal Server Error")