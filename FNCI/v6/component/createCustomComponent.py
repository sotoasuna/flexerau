'''
Created on Oct 25, 2019

@author: SGeary
'''
import logging
import requests
import json

import config


CREATE_ENDPOINT_URL = config.v6_BASEURL + "component/createCustomComponent"


logger = logging.getLogger(__name__)

#-----------------------------------------------------------------------#
def create_custom_component(component_info, authToken):
    logger.debug("Entering create_custom_component with componentId %s" %(component_info))
           
    createCustomComponentBody = get_createCustomComponentBody(component_info) 
    logger.debug("createCustomComponentBody:  %s"  %createCustomComponentBody)
      
    headers = {'Content-Type': 'application/json', 'Authorization': authToken}  
    RESTAPI_URL = CREATE_ENDPOINT_URL

    logger.debug("    RESTAPI_URL: %s" %RESTAPI_URL) 
    
    try:
        response = requests.post(RESTAPI_URL, data=createCustomComponentBody, headers=headers)
        logger.debug(json.dumps(response.json(), indent=3))  
        
    except requests.exceptions.RequestException as e:
        print(e)
        logger.debug(e)
        logger.debug(response)
        logger.debug(response.text)
        return False
    
    # Check the response code and proceed accordingly
    if response.status_code == 200:
        return True
                
    elif response.status_code == 404:
        print("Error code 404")
        return False
    
    elif response.status_code == 500:
        print("Internal Server Error")
        return False
        
        
        
def get_createCustomComponentBody(componentDetails): 
    
    componentName = componentDetails["name"]
    componentTitle = componentDetails["title"]
    forgeId = str(componentDetails["forgeId"])
    forgeName = componentDetails["forge"]
    description = componentDetails["description"]
    url = componentDetails["url"]
    encryption = componentDetails["encryption"]

    createCustomComponentBody = '''   
        {
           "name" :"''' + componentName + '''",
           "title" :"''' + componentTitle + '''",
           "url" :"''' + url + '''",
           "description" :"''' + description + '''",
            "encryption":"''' + encryption + '''",
            "componentForge" : {
                "id":"''' + forgeId + '''",
                "name":"''' + forgeName + '''"
            }
        }'''    
    
    return createCustomComponentBody    