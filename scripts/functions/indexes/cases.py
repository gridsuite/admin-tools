#
# Copyright (c) 2024, RTE (http://www.rte-france.com)
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

import requests
import constant

from ..utils import prettyprint


#
# @author Jamal KHEYYAD <jamal.kheyyad at rte-international.com>
#

def get_nb_indexed_elements():
    return requests.get(constant.GET_CASES_ELEMENTS_COUNT).text

def get_elements_index_name():
    try:
        return requests.get(constant.GET_CASES_ELEMENTS_INDEX_NAME).text
    except requests.exceptions.RequestException as e:
        print(e)
        return ""

def recreate_elements_index():
    try:
        result = requests.post(url = constant.RECREATE_CASES_ELEMENTS_INDEX)
        result.raise_for_status()
        print("Index recreated successfully.")
    except Exception as e:
        raise SystemExit(f"An error occurred while recreating the index: {e}")

def reindex_elements():    
    result = requests.post(url = constant.REINDEX_CASES_ELEMENTS)
    if not result.ok :
        print("An error occured : ")
        prettyprint(result)
