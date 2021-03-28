'''
Created on Sep 17, 2019

@author: SGeary
'''

import logging


logger = logging.getLogger(__name__)

#-----------------------------------------------------------------------#
def create_new_request(taskId, INVENTORYDETAILS):
    logger.debug("create_new_request")
    print("create a new request for taskId: %s" %taskId)
    
    componentId = INVENTORYDETAILS[1]
    componentVersionId = INVENTORYDETAILS[2]
    selectedLicenseId = INVENTORYDETAILS[3]
    
    print("   componentId: %s" %componentId)
    print("   componentVersionId: %s" %componentVersionId)
    print("   selectedLicenseId: %s" %selectedLicenseId)
    
    # Get component details from v7
    
    # Create request in v6