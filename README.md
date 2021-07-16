# workflow-integration

This python based script is an attempt to experiment with the integration of v6 workflow with v7 inventory based task actions.


pip install -r requirements.txt 

should install any missing dependencies which really is only requests since that will install
the rest.

In config.py please update all of the variables defined there to reflect the values for the 
v6 and v7 instances that are being synchronized.

In v7 the ADMIN_AUTHTKEN is required for a few of the API calls that need admin rights.  If the standard project
owner does not have admin rights enter the token for an admin user


