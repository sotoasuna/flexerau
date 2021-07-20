'''
Copyright 2020 Flexera Software LLC
See LICENSE.TXT for full license text
SPDX-License-Identifier: MIT

Author : sgeary  
Created On : Tue Feb 11 2020
File : createWorkflowDetails.py
'''
import logging
import requests
import config

logger = logging.getLogger(__name__)

FNCI_API = "FNCI Create Workflow Details API"
ENDPOINT_URL = config.BASEURL + "inventories/"

#------------------------------------------------------------------------------------------#
def update_inventory_workflow_details(inventoryId, UPDATEDETAILS, authToken):
    logger.info("Entering update_inventory_workflow_details")
    
    RESTAPI_URL = ENDPOINT_URL + str(inventoryId) + "/workflows" 
    logger.debug("    RESTAPI_URL: %s" %RESTAPI_URL)
    
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + authToken} 

    updateBody = '''
        [
            {
                "key": "Request URL",
                "value": "''' + UPDATEDETAILS[0] + '''"
            },                 
            {
                "key": "Workflow Request ID",
                "value": "''' + UPDATEDETAILS[1] + '''"
            },            
            {
                "key": "Last Activity",
                "value": "''' + UPDATEDETAILS[2] + '''"
            },
            {
                "key": "Current Review Level",
                "value": "''' + UPDATEDETAILS[3] + '''"
            },
            {
                "key": "Current Assignee",
                "value": "''' + UPDATEDETAILS[4] + '''"
            }
        ]
    '''
       
    # Make the REST API call with the project data           
    try:
        response = requests.post(RESTAPI_URL, data=updateBody, headers=headers)
    except requests.exceptions.HTTPError as errh:
        print ("HTTP Error:",errh)
        
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:",errc)

    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
        
    except requests.exceptions.RequestException as err:
        print ("Oops: Something Else",err) 
    
    # We at least received a response from FNCI so check the status to see
    # what happened if there was an error or the expected data
    if response.status_code == 200:
        logger.info("Inventory Workflow Details Updated")

    elif response.status_code == 400:
        # Bad Request
        # Assume there is no task data for the project
        logger.debug("Response code 400 - %s" %response.text)         
        
    elif response.status_code == 401:
        # Unauthorized
        logger.debug("Response code 401 - %s" %response.text) 
        
    elif response.status_code == 404:
        # Not Found
        logger.debug("Response code 404 - %s" %response.text)
        
    elif response.status_code == 405:
        # Method Not Allowed
        logger.debug("Response code 405 - %s" %response.text)
        
    elif response.status_code == 500:
        logger.debug("Response code 500 - %s" %response.text)