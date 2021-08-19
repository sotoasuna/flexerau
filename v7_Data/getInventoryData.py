'''
Copyright 2020 Flexera Software LLC
See LICENSE.TXT for full license text
SPDX-License-Identifier: MIT

Created on Sep 20, 2019

@author: SGeary
'''
import logging

import config
import FNCI.v7.projects.getProjectInventory
import FNCI.v7.inventories.getInventoryItemDetails


logger = logging.getLogger(__name__)


authToken = config.AUTHTOKEN
#------------------------------------------------------------------#

def get_v7_inventory_item_data(inventoryID, authToken):
    logger.debug("Entering get_v7_inventory_item_data with projectID: %s" %inventoryID)   
    
    
    INVENTORYDATA = FNCI.v7.inventories.getInventoryItemDetails.get_inventory_item_information_by_id(inventoryID, authToken)

    disclosed = INVENTORYDATA["disclosed"]    

    # was the item disclosed?
    if disclosed == True:
        DATA = {}

        DATA["componentId"] = INVENTORYDATA["componentId"]
        DATA["componentVersionId"] = INVENTORYDATA["componentVersionId"]
        DATA["selectedLicenseId"] = INVENTORYDATA["selectedLicenseId"]
        DATA["name"] = INVENTORYDATA["name"]
        DATA["componentName"] = INVENTORYDATA["componentName"]
        DATA["componentVersionName"] = INVENTORYDATA["componentVersionName"]
    
        
        return DATA






