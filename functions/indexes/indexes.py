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
    return requests.get(constant.GET_STUDIES_INDEXED_EQUIPMENTS_COUNT).text

def get_nb_indexed_tombstoned_equipments():
    return requests.get(constant.GET_STUDIES_INDEXED_TOMBSTONED_EQUIPMENTS_COUNT).text

def get_equipments_index_name():
    return requests.get(constant.GET_STUDIES_INDEXED_EQUIPMENTS_INDEX_NAME).text

def get_tombstoned_equipments_index_name():
    return requests.get(constant.GET_STUDIES_INDEXED_TOMBSTONED_EQUIPMENTS_INDEX_NAME).text


def delete_indexed_equipments(studyUuid):    
    result = requests.delete(url = constant.DELETE_STUDY_INDEXED_EQUIPMENTS.format(studyUuid = studyUuid))
    if not result.ok :
        print("An error occured : " + str(result.json()))

def expunge_deletes(indexName):
    print("ES Force merge : " + constant.ES_FORCE_MERGE.format(indexName = indexName) + "?only_expunge_deletes=true")
    result = requests.post(url = constant.ES_FORCE_MERGE.format(indexName = indexName), params={'only_expunge_deletes': 'true'})
