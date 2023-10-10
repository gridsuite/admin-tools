#
# Copyright (c) 2023, RTE (http://www.rte-france.com)
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

import requests
import constant

#
# @author Hugo Marcellin <hugo.marcelin at rte-france.com>
# @author Sylvain Bouzols <sylvain.bouzols at rte-france.com>
#

def get_nb_indexed_equipments():
    return requests.get(constant.GET_STUDIES_INDEXED_EQUIPMENTS_COUNT, params={}).text

def get_nb_indexed_tombstoned_equipments():
    return requests.get(constant.GET_STUDIES_INDEXED_TOMBSTONED_EQUIPMENTS_COUNT, params={}).text

def delete_indexed_equipments(studyUuid):    
    result = requests.delete(url = constant.DELETE_STUDY_INDEXED_EQUIPMENTS.format(studyUuid = studyUuid), params={})
    if not result.ok :
        print("An error occured : " + str(result.json()))
