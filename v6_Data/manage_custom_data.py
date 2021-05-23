'''
Created on Oct 28, 2019

@author: SGeary
'''

import logging
import FNCI.v6.component.associateLicenseToComponent

import v6_Data.check_custom_data
import config


logger = logging.getLogger(__name__)


def determine_custom_data(INVENTORYITEMDATA):
    logger.debug("Entering determine_custom_data")
    logger.debug("    INVENTORYITEMDATA: %s" %INVENTORYITEMDATA)
    
    
    # INVENTORYITEMDATA contains [componentId, componentVersionId, selectedLicenseId,
    #                                    name, componentName, componentVersionName ]  

    # What is being requested for use?
    componentId = INVENTORYITEMDATA["componentId"] 
    componentVersionId = INVENTORYITEMDATA["componentVersionId"]
    componentLicenseId = INVENTORYITEMDATA["selectedLicenseId"]
    componentVersionName = INVENTORYITEMDATA["componentVersionName"]

    
    #---------------------------------------------------------------------------------------#
    # Is it a custom component
    if (componentId > 1000000000):
        v6_componentId = v6_Data.check_custom_data.check_v6_custom_component(INVENTORYITEMDATA)
    else:
        # Keep using the component that was provided 
        v6_componentId = componentId
    
    #---------------------------------------------------------------------------------------#    
    # Is it a custom version
    if (componentVersionId > 1000000000):
        v6_componentVersionId = v6_Data.check_custom_data.check_v6_custom_version(v6_componentId, componentVersionId, componentVersionName)
    else:
        # Keep using the version ID that was provided
        v6_componentVersionId = componentVersionId
    
    #---------------------------------------------------------------------------------------#
    # Is it a custom license   
    if (componentLicenseId > 1000000000):
        v6_componentLicenseId = v6_Data.check_custom_data.check_v6_custom_license(v6_componentId, v6_componentVersionId, componentLicenseId)
    else:
        # Keep using the license ID that was provided
        v6_componentLicenseId = componentLicenseId
        
    # We now have of the v7 to v6 mappings for the workflow data
    logger.debug("We have the mapped IDs from v6")
    logger.debug("    Component IDs   v7: %s  --->  v6: %s" %(componentId, v6_componentId))
    logger.debug("    Version IDs     v7: %s  --->  v6: %s" %(componentVersionId, v6_componentVersionId))
    logger.debug("    License IDs     v7: %s  --->  v6: %s" %(componentLicenseId, v6_componentLicenseId))
    
    # Associate the license to the component
    # For now just try to associate it no matter what  
    FNCI.v6.component.associateLicenseToComponent.associate_license_to_component(v6_componentId, v6_componentLicenseId, config.v6_AUTHTOKEN)
    
    
    return [v6_componentId, v6_componentVersionId, v6_componentLicenseId ]
