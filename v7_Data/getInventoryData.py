'''
Created on Sep 20, 2019

@author: SGeary
'''
import logging

import config
import FNCI.v7.projects.getProjectInventory


logger = logging.getLogger(__name__)


authToken = config.AUTHTOKEN
#------------------------------------------------------------------#

def get_v7_inventory_data(projectID):
   
    INVENTORYITEMS = {}     
    
    logger.debug("Entering get_v7_inventory_data with projectID: %s" %projectID)   
     
    INVENTORY = FNCI.v7.projects.getProjectInventory.get_project_inventory(projectID, authToken) 

    #--------------------------------------------------------------------------#    
    # Create a dictionary containing key information about the inventory item    
    for inventoryITEM in INVENTORY:
        inventoryItemId = inventoryITEM["id"]
        componentId = inventoryITEM["componentId"]
        componentVersionId = inventoryITEM["componentVersionId"]
        selectedLicenseId = inventoryITEM["selectedLicenseId"]
        disclosed = inventoryITEM["disclosed"]
        componentName = inventoryITEM["name"]
        
        # was the item disclosed?
        if disclosed == True:
            
            INVENTORYITEMS[inventoryItemId] = [componentId, componentVersionId, selectedLicenseId, componentName]
            
    return INVENTORYITEMS



