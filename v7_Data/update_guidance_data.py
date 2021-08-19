'''
Copyright 2020 Flexera Software LLC
See LICENSE.TXT for full license text
SPDX-License-Identifier: MIT

Created on Dec 11, 2019

@author: SGeary
'''

import logging

import FNCI.v7.inventories.updateInventory


logger = logging.getLogger(__name__)


#------------------------------------------------------------#
def update_v7_guidance_notes(inventoryId, licenseName, OBLIGATIONDATA, authToken):
    
    # Need to create HTML data for the guidance from the obligation data
    print(licenseName)
    guidanceText = ''' <b>License Name: </b>''' + licenseName + '''<br>'''
   
    for obligation in OBLIGATIONDATA:
        print(obligation)
        print(OBLIGATIONDATA[obligation])


    FNCI.v7.inventories.updateInventory.update_inventory_item_UsageGuidance(inventoryId, guidanceText, authToken)
