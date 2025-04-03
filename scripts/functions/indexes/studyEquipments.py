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
# @author Hugo Marcellin <hugo.marcelin at rte-france.com>
# @author Sylvain Bouzols <sylvain.bouzols at rte-france.com>
#

def get_nb_indexed_studies():
    return requests.get(constant.GET_STUDIES_INDEXED_STUDIES_COUNT).text

def get_nb_indexed_equipments():
    return requests.get(constant.GET_STUDIES_INDEXED_EQUIPMENTS_COUNT).text

def get_nb_indexed_tombstoned_equipments():
    return requests.get(constant.GET_STUDIES_INDEXED_TOMBSTONED_EQUIPMENTS_COUNT).text

def get_studies_index_name():
    try:
        return requests.get(constant.GET_STUDIES_INDEXED_STUDIES_INDEX_NAME).text
    except requests.exceptions.RequestException as e:
        print(e)
        return ""

def get_equipments_index_name():
    try:
        return requests.get(constant.GET_STUDIES_INDEXED_EQUIPMENTS_INDEX_NAME).text
    except requests.exceptions.RequestException as e:
        print(e)
        return ""

def get_tombstoned_equipments_index_name():
    try:
        return requests.get(constant.GET_STUDIES_INDEXED_TOMBSTONED_EQUIPMENTS_INDEX_NAME).text
    except requests.exceptions.RequestException as e:
        print(e)
        return ""

def recreate_study_indices():
    try:
        result = requests.post(url = constant.RECREATE_STUDY_INDICES)
        result.raise_for_status()
        print("Study indices recreated successfully.")
    except Exception as e:
        raise SystemExit(f"An error occurred while recreating study indices: {e}")

def reindex_study_and_equipments(study_uuid):
    result = requests.post(url = constant.REINDEX_STUDY_AND_EQUIPMENTS.format(studyUuid = study_uuid))
    if not result.ok :
        print("An error occured : ")
        prettyprint(result)
