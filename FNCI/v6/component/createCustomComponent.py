'''
Copyright 2020 Flexera Software LLC
See LICENSE.TXT for full license text
SPDX-License-Identifier: MIT

Created on Oct 25, 2019

@author: SGeary
'''
import logging
import requests
import sys
import config

logger = logging.getLogger(__name__)

#######################################################################
# If the calling app is a flask app then we can use
# the flask abort function to catch exceptions
# so see if its defined in a common config file
try: 
    FLASKAPP = config.FLASKAPP
except:
    FLASKAPP = False

if FLASKAPP:
    from flask import abort
#######################################################################

FNCI_API = "FNCI v6 Create Custom Component API"
ENDPOINT_URL = config.v6_BASEURL + "component/createCustomComponent"

#-----------------------------------------------------------------------#
def create_custom_component(component_info, authToken):
    logger.debug("Entering create_custom_component with componentId %s" %(component_info))
           
    createCustomComponentBody = get_createCustomComponentBody(component_info) 
    logger.debug("createCustomComponentBody:  %s"  %createCustomComponentBody)
      
    headers = {'Content-Type': 'application/json', 'Authorization': authToken}  
    RESTAPI_URL = ENDPOINT_URL

    logger.debug("    RESTAPI_URL: %s" %RESTAPI_URL) 
    
    try:
        response = requests.post(RESTAPI_URL, data=createCustomComponentBody, headers=headers)
        response.raise_for_status() 
        
    except requests.exceptions.ConnectionError:
        # Connection Error - Is the server up and running?
        abort_message = FNCI_API + " - Error Connecting to FNCI Server - " +  (ENDPOINT_URL).split("palamida")[0] # Get rid of everything after palamida in url
        logger.error("    %s" %(abort_message))

        if FLASKAPP:         
            # Using error code 500 (Internal Server Error) to cover connection errors
            # in the flask apps
            abort(500, FNCI_API + " - %s" %abort_message) 
        else:
            print(abort_message)
            print("Is the FNCI server running?")
            print("Exiting script")
            sys.exit() 
    except requests.exceptions.RequestException as e: # Catch the exception for the logs but process below
        logger.error(e)
    
    # We at least received a response from FNCI so check the status to see
    # what happened if there was an error or the expected data
    if response.status_code == 200:
        logger.debug("    Call to %s was successful." %FNCI_API)
        # We created the component so grab the ID to return
        v6_componentId = response.json()["Id"]
        return v6_componentId
                
    elif response.status_code == 400:
        # Bad Request
        logger.error("Response code 400 - %s" %response.text)
        if FLASKAPP:         
            abort(400, FNCI_API + " - Bad Request - Look at debug log for more details") 
        else:
            print("%s - Error: %s -  Bad Request." %(FNCI_API, response.status_code ))
            print("    Exiting script")
            sys.exit()   

    elif response.status_code == 401:
        # Unauthorized Access
        logger.error("    %s - Error: %s -  Authentication Failed: JWT token is not valid or user does not have correct permissions." %(FNCI_API, response.status_code ))
        if FLASKAPP:         
            abort(401, FNCI_API + " - Authentication Failed: JWT token is not valid or user does not have correct permissions.")
        else:
            print("%s - Error: %s -  Authentication Failed: JWT token is not valid or user does not have correct permissions." %(FNCI_API, response.status_code ))
            print("    Exiting script")
            sys.exit()   

    elif response.status_code == 404:
        # Not Found
        logger.error("    %s - Error: %s -  URL endpoint not found:  %s" %(FNCI_API, response.status_code,  RESTAPI_URL ))
        if FLASKAPP:         
            abort(400, FNCI_API + " - Bad Request - URL endpoint not found") 
        else:
            print("    %s - Error: %s -  URL endpoint not found:  %s" %(FNCI_API, response.status_code,  RESTAPI_URL ))
            print("    Exiting script")
            sys.exit()   

    elif response.status_code == 405:
        # Method Not Allowed
        logger.error("    %s - Error: %s -  Method (GET/POST/PUT//DELETE/ETC) Not Allowed." %(FNCI_API, response.status_code ))
        if FLASKAPP:         
            abort(405, FNCI_API + " - Method Not Allowed.")
        else:
            print("    %s - Error: %s -  Method (GET/POST/PUT//DELETE/ETC) Not Allowed." %(FNCI_API, response.status_code ))
            print("    Exiting script")
            sys.exit()  
        
    elif response.status_code == 500:
        # Internal Server Error
        logger.error("    %s - Error: %s -  Internal Server Error." %(FNCI_API, response.status_code ))
        if FLASKAPP:         
            abort(500, FNCI_API + " - Internal Server Error.")
        else:
            print("    %s - Error: %s -  Internal Server Error." %(FNCI_API, response.status_code ))
            print("    Exiting script")
            sys.exit()  
        
        
        
        
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