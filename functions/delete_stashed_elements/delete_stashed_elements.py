#
# Copyright (c) 2024, RTE (http://www.rte-france.com)
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

import requests
import constant

#
# @author Kevin Le Saulnier <kevin.lesaulnier at rte-france.com>
#

# print element description
def deleted_element_described(element):
    return " - type: " + element["type"] + ", elementName: " + element["elementName"] + ", elementUuid: " + element["elementUuid"] 

# delete all stashed element - BE AWARE, directories are not recursively emptied, only stashed elements are deleted
def delete_stashed_elements(dry_run):
    print("/// stashed elements deletion ///")
    stashed_elements = requests.get(constant.GET_DIRECTORY_STASHED_ELEMENTS).json()
    print(stashed_elements)
    print("Here are the elements that will be deleted")
    print("\n".join(map(deleted_element_described, stashed_elements)))
    if not dry_run :
        data = {'ids': list(map(lambda element: element["elementUuid"], stashed_elements))}
        result = requests.delete(constant.DELETE_EXPLORE_ELEMENTS, params=data, headers={"userId": "supervision"})
        if result.ok :
            print("Elements were deleted with success")
        else :
            print("An error occurred with status code:", result.status_code)

