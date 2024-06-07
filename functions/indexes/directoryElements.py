#
# Copyright (c) 2024, RTE (http://www.rte-france.com)
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

import requests
import constant

#
# @author Sylvain Bouzols <sylvain.bouzols at rte-france.com>
#

def get_nb_indexed_elements():
    return requests.get(constant.GET_DIRECTORY_ELEMENTS_COUNT).text

def get_elements_index_name():
    try:
        return requests.get(constant.GET_DIRECTORY_ELEMENTS_INDEX_NAME).text
    except requests.exceptions.RequestException as e:
        print(e)
        return ""

def delete_indexed_elements():    
    result = requests.delete(url = constant.DELETE_INDEXED_ELEMENTS)
    if not result.ok :
        print("An error occured : " + str(result.json()))

def reindex_elements():    
    result = requests.post(url = constant.REINDEX_ELEMENTS)
    if not result.ok :
        print("An error occured : " + str(result.json()))

