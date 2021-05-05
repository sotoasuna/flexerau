'''
Created on Sep 21, 2019

@author: SGeary
'''
import logging
import json
import os

import config

logger = logging.getLogger(__name__)

def get_historical_RTI_mappings(projectID):
    logger.debug("Entering get_historical_RTI_mappings with projectID of %s" %projectID)
    
    # The file name containing the data will change depending on the projectID  
   
    RTI_MAPPINGS_FILE = config.RTI_MAPPINGS_DIRECTORY + "project" + str(projectID) +  "_" + config.RTI_MAPPINGS_FILE_SUFFIX

    # Set up a dictionary to hold a mapping between v7 tasks and v7 workflow
    INVENTORYITEM_REQUESTS = {}    
    try:
        PREVIOUS_REQUESTS = json.loads(open(RTI_MAPPINGS_FILE).read())
        logger.debug("Opening %s file for request that are currently being tracked for this project" %RTI_MAPPINGS_FILE)
    
        for existing_request in PREVIOUS_REQUESTS["requests"]:
            # There are the specific requests for this project
            INVENTORYITEM_REQUESTS[existing_request["v7_taskId"]] = [existing_request["v7_inventoryId"], existing_request["v6_request"]]
    
        logger.debug("Returning RTI Mappings for project %s" %projectID)
        return INVENTORYITEM_REQUESTS
  
    except:
        # The script so far has not run with any tasks to process
        logger.debug("%s file does not exist currently" %RTI_MAPPINGS_FILE)
        return INVENTORYITEM_REQUESTS  # Just return an empty dictionary
 
def update_RTI_mappings(projectID, EXISTING_RTI_MAPPINGS):
   
    logger.debug("Entering update_RTI_mappings with projectID of %s" %projectID)
    
    if not os.path.exists(config.RTI_MAPPINGS_DIRECTORY):
        os.makedirs(config.RTI_MAPPINGS_DIRECTORY)
       
    RTI_MAPPINGS_FILE = config.RTI_MAPPINGS_DIRECTORY + "project" + str(projectID) +  "_" + config.RTI_MAPPINGS_FILE_SUFFIX
    logger.debug("Updating %s" %RTI_MAPPINGS_FILE )     
               
    RTI_MAPPINGS = {}
    RTI_MAPPINGS["requests"] = []
    
    for taskId in EXISTING_RTI_MAPPINGS:
        RTI_MAPPINGS['requests'].append({
        'v7_inventoryId': EXISTING_RTI_MAPPINGS[taskId][0],
        'v7_taskId': taskId,
        'v6_request': EXISTING_RTI_MAPPINGS[taskId][1]
        })  

    
    # Now write the data back out to the file        
    with open(RTI_MAPPINGS_FILE, 'w') as outfile:
        json.dump(RTI_MAPPINGS, outfile, indent=3) 
    
