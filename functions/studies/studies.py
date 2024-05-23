#
# Copyright (c) 2023, RTE (http://www.rte-france.com)
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

import requests
import constant
import logging

#
# @author Sylvain Bouzols <sylvain.bouzols at rte-france.com>
#

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_all_studies_uuid():
    return requests.get(constant.GET_STUDIES).json()

def get_all_orphan_indexed_equipments_count():
    return requests.get(constant.GET_ALL_ORPHAN_INDEXED_EQUIPMENTS_COUNT).text
def delete_all_orphan_indexed_equipments():
    try:
        result = requests.delete(constant.DELETE_ALL_ORPHAN_INDEXED_EQUIPMENTS_COUNT)

        # Check if the response status code indicates success
        if result.status_code == 200:
            logger.info("Successfully deleted all orphan indexed equipments.")
            return True
        else:
            logger.error(f"Failed to delete orphan indexed equipments: {result.status_code} - {result.text}")
            return False
    except requests.exceptions.RequestException as e:
        logger.exception("Exception occurred while deleting orphan indexed equipments: " + str(e))
        return False

def invalidate_nodes_builds(studyUuid):
    return requests.delete(constant.DELETE_STUDY_NODES_BUILDS.format(studyUuid = studyUuid))

def check_status_study_server():
    try:
        result = requests.get(constant.GET_ACTUATOR_INFO)

        if not result.ok :
            # TODO this might not be a json format
            print("An error occured : " + str(result.json()))
            return False
        status = result.json()
        print("-----------------------")
        print("study-server describe-short : " + status['git']['commit']['id']['describe-short'])
        print("study-server name : " + status['build']['name'])
        print("study-server version : " + status['build']['version'])
        return True
    except requests.exceptions.RequestException as e:
        print("Exception during study-server check status")
        print(e)
        return False
    
