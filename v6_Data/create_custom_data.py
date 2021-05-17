'''
Created on Oct 25, 2019

@author: SGeary
'''
import logging

import FNCI.v6.component.createCustomComponent
import FNCI.v6.component.createCustomVersion
import FNCI.v6.component.componentDataFiltered
import FNCI.v6.component.componentVersionDataByName
import FNCI.v6.component.createLicense

import FNCI.v7.license.lookupLicense

import config

logger = logging.getLogger(__name__)

v6_authToken = config.v6_AUTHTOKEN
v7_authToken = config.AUTHTOKEN


#---------------------------------------------------------------------------------#
def create_v6_custom_component(componentData):
    logger.debug("Entering create_v6_custom_component")
    logger.debug("v7 componentData: %s" %componentData)


    # Make REST API call with provided data
    if FNCI.v6.component.createCustomComponent.create_custom_component(componentData, v6_authToken):
    # The ID is not returned to search for the component based on a filtered request
    
        componentName = componentData["name"]
        componentTitle = componentData["title"]
        v6_component_data = FNCI.v6.component.componentDataFiltered.get_filtered_component_data_by_name_and_title(componentName, componentTitle, v6_authToken)
        
        for component in v6_component_data["components"]:
                name = component["name"]
                title = component["title"]
                
                if name == componentName and title == componentTitle:
                    # This is the one we want
                    v6_componentId = component["id"]
                    logger.debug("Component %s created with an ID of %s" %(componentName, v6_componentId))
                    return v6_componentId    
    else:
        print("the was an issue creating the custom component")    
 
    
    
    
    
#---------------------------------------------------------------------------------#
def create_v6_custom_version(componentID, componentVersionName):
    logger.debug("Entering create_v6_custom_version")
    logger.debug("componentID: %s  componentVersionName: %s" %(componentID, componentVersionName))
    
    # Create the customer component
    versionCreated = FNCI.v6.component.createCustomVersion.create_custom_component_version(componentID, componentVersionName, v6_authToken)
    
    if versionCreated:
        # The ID is not returned to search for the version ID
        componentVersionID = FNCI.v6.component.componentVersionDataByName.get_component_version_data_by_name(componentID, componentVersionName, v6_authToken)
        v6_componentVersionID =  componentVersionID["id"]
        
        logger.debug("Version %s created for component %s with an ID of %s" %(componentVersionName, componentID, v6_componentVersionID))
        
        return v6_componentVersionID
    else:
        return False
    
    
#---------------------------------------------------------------------------------#
def create_v6_custom_license(componentID, componentVersionID, componentLicenseId):
    logger.debug("Entering create_v6_custom_license")
    logger.debug("componentID: %s  componentVersionID: %s  componentLicenseId: %s  " %(componentID, componentVersionID, componentLicenseId))
    
    # Get license information from v7
    
    v7_license_details = FNCI.v7.license.lookupLicense.lookup_license(componentLicenseId, v7_authToken)
    
    # Make REST API call with provided data
    v6_componentLicenseId = FNCI.v6.component.createLicense.create_custom_license(v7_license_details, v6_authToken)

    return v6_componentLicenseId
    
    
    
    