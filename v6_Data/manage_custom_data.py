'''
Created on Oct 28, 2019

@author: SGeary
'''

import logging
import FNCI.v6.component.associateLicenseToComponent
import FNCI.v6.component.createCustomComponent
import FNCI.v6.component.createCustomVersion
import FNCI.v6.component.createLicense

import FNCI.v7.component.getComponent
import FNCI.v7.license.lookupLicense

import config
v6_authToken = config.v6_AUTHTOKEN
v7_authToken = config.AUTHTOKEN

logger = logging.getLogger(__name__)


def determine_custom_data(INVENTORYITEMDATA):
    logger.debug("Entering determine_custom_data")
    logger.debug("    INVENTORYITEMDATA: %s" %INVENTORYITEMDATA)

    # What is being requested for use?
    componentId = INVENTORYITEMDATA["componentId"] 
    componentVersionId = INVENTORYITEMDATA["componentVersionId"]
    componentLicenseId = INVENTORYITEMDATA["selectedLicenseId"]
    componentVersionName = INVENTORYITEMDATA["componentVersionName"]

    
    #---------------------------------------------------------------------------------------#
    # Is it a custom component
    if (componentId > 1000000000):
        # If the component that matches the v7 component with the supplied componentId
        # exists the error will return the component ID and if the component does
        # not exist it will be created and the component ID will be returned
        v7_component_details = FNCI.v7.component.getComponent.get_component_information_by_id(componentId, v7_authToken)
    
        # The API will return the ID if newly created or if it was already created
        # it will also return the ID in the error message
        v6_componentId =  FNCI.v6.component.createCustomComponent.create_custom_component(v7_component_details, v6_authToken)

    else:
        # Keep using the component that was provided 
        v6_componentId = componentId
    
    #---------------------------------------------------------------------------------------#    
    # Is it a custom version
    if (componentVersionId > 1000000000):
        
        # If the version of the component that matches the v7 component/version name
        # exists the error will return the componentVersionId and if the component does
        # not exist it will be created and the componentVersionId will be returned
        v6_componentVersionId = FNCI.v6.component.createCustomVersion.create_custom_component_version(v6_componentId, componentVersionName, v6_authToken)
    
    else:
        # Keep using the version ID that was provided
        v6_componentVersionId = componentVersionId
    
    #---------------------------------------------------------------------------------------#
    # Is it a custom license   
    if (componentLicenseId > 1000000000):
        # If the license exists the error will return the license ID and if
        # the license does not exist it will be created and the license ID will be returned
        # Get license information from v7   
        v7_license_details = FNCI.v7.license.lookupLicense.lookup_license(componentLicenseId, v7_authToken)
    
        # Make REST API call with provided data
        v6_componentLicenseId = FNCI.v6.component.createLicense.create_custom_license(v7_license_details, v6_authToken)

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
