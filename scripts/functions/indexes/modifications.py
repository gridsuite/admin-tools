#
# Copyright (c) 2025, RTE (http://www.rte-france.com)
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

import requests
import constant

from ..utils import prettyprint


#
# @author Kevin Le Saulnier <kevin.lesaulnier at rte-france.com>
#

def get_nb_indexed_modifications():
    return requests.get(constant.GET_MODIFICATIONS_ELEMENTS_COUNT).text

def get_nb_modifications_to_index():
    return requests.get(constant.GET_MODIFICATIONS_ELEMENTS_TO_INDEX_COUNT).text

def get_modifications_index_name():
    try:
        return requests.get(constant.GET_MODIFICATIONS_INDEX_NAME).text
    except requests.exceptions.RequestException as e:
        print(e)
        return ""

def recreate_modifications_index():
    try:
        result = requests.post(url = constant.RECREATE_MODIFICATIONS_INDEX)
        result.raise_for_status()
        print("Index recreated successfully.")
    except Exception as e:
        raise SystemExit(f"An error occurred while recreating the index: {e}")

def reindex_modifications():    
    result = requests.post(url = constant.REINDEX_MODIFICATIONS)
    if not result.ok :
        print("An error occured : ")
        prettyprint(result)
